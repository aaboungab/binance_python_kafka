from confluent_kafka import Consumer, KafkaError
import avro.schema
from avro.io import DatumReader
import io

def consume_avro_data(bootstrap_servers,topic,group):
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
    avro_schema = avro.schema.parse(schema_str)

    # Create consumer configuration
    conf = {'bootstrap.servers': bootstrap_servers,
            'group.id': group,
            'auto.offset.reset': 'earliest'}

    # Create Consumer instance
    consumer = Consumer(conf)

    # Subscribe to the topic
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                print("Consumer error: {}".format(msg.error()))
                continue
            else:
                response = {}
                response['topic']= msg.topic()
                response['partition']= msg.partition()
                response['offset']= msg.offset()
                print(f"\nResponse: {response}")

            # Deserialize the Avro data
            bytes_reader = io.BytesIO(msg.value())
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(avro_schema)
            message = reader.read(decoder)
            print(f"Message: {message}\n")

            # return message

    except KeyboardInterrupt:
        pass

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()

# while True:
bootstrap_servers = 'localhost:9092'
topic = 'binance_btc_data'
group = 'binance-group'
consume_avro_data(bootstrap_servers,topic,group)