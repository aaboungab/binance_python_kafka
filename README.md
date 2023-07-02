# Python, Binance & Kafka
This repo contains python scripts for interacting with Kafka cluster and producing avro binance data of various crypto currencies

## Prerequisites

- Python 3.x installed
- Install required python libaries in reqiurements.txt
 ```python
pip install -r requirements.txt
```
- Binance account with your own api key and secret. 
 ```bash
 # linux commands to export vars containing binance account credentials
export binance_api_keu=YOUR_API_KEY
export binance_api_secret=YOUR_SECRET_KEY
```
 ```powershell
 # windows powershell commands to export vars containing binance account credentials
set binance_api_key=YOUR_API_KEY
set binance_api_secret=YOUR_SECRET_KEY
```
- Running Kafka cluster (single or multinode)
    - You can use the provided  [docker compose]() file to launch a multi node Confluent Kafka cluster. Servies used:
        1. Zookeeper
        2. Broker
        3. Schema Registry
        4. Control Center (cluster monitoring)