import argparse
from confluent_kafka.admin import AdminClient, ConfigResource

def list_topics(bootstrap_servers):
    conf = {'bootstrap.servers': bootstrap_servers}
    client = AdminClient(conf)
    
    metadata = client.list_topics(timeout=10)
    print(f"Topics for cluster at {bootstrap_servers}: ")
    for t in metadata.topics.values():
        # print(f'topic: {t.topic}\npartitions: {t.partitions.items()}\n')
        if not t.topic.startswith('_'):
            print(dir(t.partitions))
            print(f'topic: {t.topic}\npartitions: {t.partitions.items()}\n')

def describe_topic(bootstrap_servers, topic):
    conf = {'bootstrap.servers': bootstrap_servers}
    client = AdminClient(conf)

    resources = [ConfigResource(ConfigResource.Type.TOPIC, topic)]
    configs = client.describe_configs(resources, request_timeout=20)

    for resource, config in configs.items():
        print(f"\nConfig details for topic {topic}: ")
        for config_entry in config.result().values():
            print(f"\t{config_entry.name}: {config_entry.value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List and describe topics in a Kafka cluster.")
    parser.add_argument("-b", "--bootstrap-servers", required=True, help="The bootstrap servers, comma separated.")
    parser.add_argument("-d", "--describe", action="store_true", help="Describe the topic specified by -t.")
    parser.add_argument("-t", "--topic", type=str, help="The topic to describe.")
    args = parser.parse_args()

    if args.describe:
        if args.topic:
            describe_topic(args.bootstrap_servers, args.topic)
        else:
            print("-d flag must be used with -t TOPIC_NAME if you want to describe a topic")
    else:
        list_topics(args.bootstrap_servers)

