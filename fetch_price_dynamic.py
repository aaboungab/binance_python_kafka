import os
import pandas as pd
from binance.client import Client
from termcolor import colored
import time

# Set up your Binance API credentials
api_key = os.getenv('binance_api_key')
api_secret = os.getenv('binance_api_secret')
client = Client(api_key, api_secret)

# Define the start date and end date for your data retrieval
start_date = '2017-01-01'   # Replace with your desired start date
end_date = '2023-07-22'  # Replace with your desired end date

# Function to fetch data and store it in the directory for a specific symbol
def fetch_data_and_store(symbol):
    # Create the directory for the symbol if it doesn't exist
    symbol_dir = os.path.join('data', symbol)
    if not os.path.exists(symbol_dir):
        os.makedirs(symbol_dir)

    # Retrieve ticket data for each year in the date range
    date_range = pd.date_range(start=start_date, end=end_date, freq='YS')

    symbol_data = {}  # Dictionary to store data for the symbol
    for i in range(len(date_range)-1):
        interval_start = date_range[i].strftime('%Y-%m-%d')
        interval_end = date_range[i+1].strftime('%Y-%m-%d')
        # print(f"Working on {symbol}")
        ticket_data = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, interval_start, interval_end)

        # Check if there is data available for the current interval
        if ticket_data:
            # Convert timestamp to datetime and select relevant columns
            df = pd.DataFrame(ticket_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df = df[['datetime', 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'number_of_trades']]

            # Validate data
            year = date_range[i].year
           
            print(f'{colored(year, "yellow")} data saved to CSV')
            print("\033[1A", end="")
            time.sleep(1)

            # Save to CSV
            csv_file_name = os.path.join(symbol_dir, f"{symbol}_{year}_price.csv")
        
            
            
            df.to_csv(csv_file_name, index=False)

            # Load data from CSV to dictionary
            symbol_data[year] = pd.read_csv(csv_file_name, parse_dates=['datetime'])

    return symbol_data

# Define the focus_symbols variable with the symbols you want to fetch data for (can be one or many symbols)
focus_symbols = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "LTCUSDT"]

# Dictionary to store data for each symbol
all_symbol_data = {}

# Fetch data and store it in the directory for each symbol in the focus_symbols list
for symbol in focus_symbols:
    print(f'Working on {colored(symbol, "yellow")}')
    all_symbol_data[symbol] = fetch_data_and_store(symbol)
    print(f'finished working on {colored(symbol, "green")}')
    time.sleep(5)