from binance import Client
import json
import avro.schema
import io
from confluent_kafka import Producer, KafkaError
from datetime import datetime
from avro.io import DatumWriter
from confluent_kafka.schema_registry import SchemaRegistryClient
import time
import os

api_key = os.getenv('binanace_api_key')
api_secret = os.getenv('binance_api_secret')
client = Client(api_key, api_secret)
symbol = ["BTCUSDT","ETHUSDT","XRPUSDT","DOGEUSDT","LTCUSDT"]
bootstrap_servers = "localhost:9092"  # Replace with your Kafka broker address
topic = 'binance_btc_data'
# symbol = ["BTCUSDT"]

def get_ticker(symbol):
    data = {}
    ticker = client.get_ticker(symbol=symbol)
    data['current_timestamp'] = datetime.now().replace(second=0, microsecond=0).isoformat()
    data['symbol'] = ticker['symbol']
    data['openPrice'] = float(ticker['openPrice'])
    data['highPrice'] = float(ticker['highPrice'])
    data['lowPrice'] = float(ticker['lowPrice'])
    data['prevClosePrice'] = float(ticker['prevClosePrice'])
    json_data = json.dumps(data)
    return json_data

def send_avro_to_kafka(json_data):
    schema_str = """
    {
    "namespace": "binance.avro",
    "type": "record",
    "name": "Ticker",
    "fields" : [
        {"name": "current_timestamp", "type": "string"},
        {"name": "symbol", "type": "string"},
        {"name": "openPrice", "type": "float"},
        {"name": "highPrice", "type": "float"},
        {"name": "lowPrice", "type": "float"},
        {"name": "prevClosePrice", "type": "float"}
    ]
    }
    """
    avro_schema = avro.schema.Parse(schema_str)

    # Convert JSON to Avro
    writer = avro.io.DatumWriter(avro_schema)
    bytes_writer = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_writer)
    writer.write(json.loads(json_data), encoder)

    avro_data = bytes_writer.getvalue()
    
    # Kafka producer configuration
    conf = {'bootstrap.servers': 'localhost:9092'}
    schema_conf = {'url' : 'http://0.0.0.0:8081'}
    schema_registry_client = SchemaRegistryClient(schema_conf)
    p = Producer(conf)
    try:
        p.produce(topic,value=avro_data)
        print(f"record sent!\nJSON format: {json_data}\nAVRO format: {avro_data}")
        p.flush()
    except KafkaError as e:
        print(f"failed with exception {e}")
    except KeyboardInterrupt:
        print('\t\tAborted by user\n')
        
while True:
    for i in symbol:
        data = get_ticker(i)
        send_avro_to_kafka(data)
    time.sleep(30)