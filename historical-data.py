import boto3
from botocore.exceptions import NoCredentialsError
from binance.client import Client
from datetime import datetime, timedelta
import pandas as pd
import os

def retrieve_historical_klines(api_key, api_secret, symbols):
    # Create a Binance client
    client = Client(api_key, api_secret)

    # Calculate the start and end dates for the historical data
    end_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=365)

    # Create an S3 client
    s3 = boto3.client('s3')
    
    for symbol in symbols:
        # Retrieve the historical K-line data for each symbol
        klines = client.futures_klines(
            symbol=symbol,
            interval=Client.KLINE_INTERVAL_1DAY,
            startTime=int(start_date.timestamp() * 1000),
            endTime=int(end_date.timestamp() * 1000)
        )

        # Create a list of dictionaries to store K-line data for the current symbol
        symbol_data = []
        for kline in klines:
            timestamp = datetime.fromtimestamp(int(kline[0]) / 1000)
            symbol_data.append({
                'symbol': symbol,
                'timestamp': timestamp,
                'open_price': float(kline[1]),
                'high_price': float(kline[2]),
                'low_price': float(kline[3]),
                'close_price': float(kline[4]),
                'volume': float(kline[5])
            })

        # Create a Pandas DataFrame from the symbol's K-line data
        df = pd.DataFrame(symbol_data)


        # Calculate and add moving averages to the DataFrame
        calculate_moving_averages(df)
        
        # Format the prices with a dollar sign, commas, and two decimal places
        df['open_price'] = df['open_price'].apply(lambda x: '${:,.2f}'.format(x))
        df['high_price'] = df['high_price'].apply(lambda x: '${:,.2f}'.format(x))
        df['low_price'] = df['low_price'].apply(lambda x: '${:,.2f}'.format(x))
        df['close_price'] = df['close_price'].apply(lambda x: '${:,.2f}'.format(x))

        # Generate the CSV data as a string
        csv_data = df.to_csv(index=False)
        
        # Generate the S3 object key
        object_key = f'365d_{symbol}_price.csv'
        
        # Upload the CSV data to S3
        upload_to_s3(csv_data, s3, bucket_name='my-data-bucket-aa-s3', object_key=object_key)


def calculate_moving_averages(df):
    # Calculate moving averages (10, 20, 50, 100)
    df['ma10'] = df['close_price'].rolling(window=10).mean().apply(lambda x: '${:,.2f}'.format(x))
    df['ma20'] = df['close_price'].rolling(window=20).mean().apply(lambda x: '${:,.2f}'.format(x))
    df['ma50'] = df['close_price'].rolling(window=50).mean().apply(lambda x: '${:,.2f}'.format(x))
    df['ma100'] = df['close_price'].rolling(window=100).mean().apply(lambda x: '${:,.2f}'.format(x))

def upload_to_s3(data, s3, bucket_name, object_key):
    try:
        s3.put_object(Body=data, Bucket=bucket_name, Key=object_key)
        print(f'Successfully uploaded data to S3 bucket: {bucket_name} with key: {object_key}')
    except NoCredentialsError:
        print('AWS credentials not found.')     
   
# Replace with your Binance API keys
api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')

# Define the list of symbols
symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "LTCUSDT"]

# Retrieve and save the historical K-line data for each symbol
retrieve_historical_klines(api_key, api_secret, symbols)
