# Python, Binance & Kafka
This repo contains python scripts for interacting with Kafka cluster and producing Avro Binance data of various crypto currencies/

## Prerequisites

- Python 3.x installed
- Install required python libaries in reqiurements.txt
 ```python
pip install -r requirements.txt
```
- Binance account with your own api key and secret. 
 ```bash
 # linux commands to export vars containing binance account credentials
export binance_api_key=YOUR_API_KEY
export binance_api_secret=YOUR_SECRET_KEY
```
 ```powershell
 # windows powershell commands to export vars containing binance account credentials
set binance_api_key=YOUR_API_KEY
set binance_api_secret=YOUR_SECRET_KEY
```
- Running Kafka cluster (single or multinode)
    - You can use the provided  [docker compose](https://github.com/aaboungab/binance_python_kafka/blob/main/docker-compose.yaml) file to launch a multi node Confluent Kafka cluster. Services used:
        1. Zookeeper
        2. Broker
        3. Schema Registry
        4. Control Center (cluster monitoring)

## List and describe topics
To list topics or describe any topic use the list-topics.py script
```python
usage: list-topics.py [-h] -b BOOTSTRAP_SERVERS [-d] [-t TOPIC]

# list all topics
python list-topics.py -b localhost:9092

# describe topic specified using -t flag
python list-topics.py -b localhost:9092-d -t binance_btc_data
```

## Start producer
Start producer by running avro-producer.py to produce data into the Kafka cluster
```python
python avro-producer.py
```
Example output:
```python
record sent!
JSON format: {"current_timestamp": "2023-07-02T03:56:00", "symbol": "BTCUSDT", "openPrice": 30420.54, "highPrice": 30661.6, "lowPrice": 30320.57, "prevClosePrice": 30420.53}
AVRO format: b'&2023-07-02T03:56:00\x0eBTCUSDT\x14\xa9\xedF3\x8b\xefF$\xe1\xecF\x0f\xa9\xedF'
``` 
## Start Consumer
Start consumer to consume records from a topic
```python
python avro-consumer.py
```
Example output:
```python
Response: {'topic': 'binance_btc_data', 'partition': 0, 'offset': 124}
Message: {'current_timestamp': '2023-07-02T04:24:00', 'symbol': 'ETHUSDT', 'openPrice': 1920.1500244140625, 'highPrice': 1929.8699951171875, 'lowPrice': 1909.43994140625, 'prevClosePrice': 1920.1500244140625}
```

# Purpose
The primary purpose of this program is to provide a practical demonstration and learning experience of interacting with a Kafka cluster using Python libraries as both a producer and a consumer. Kafka is an incredibly versatile tool that offers a wide range of capabilities, including data processing and streaming, data retention, and data availability.
