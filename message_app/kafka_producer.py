import json
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer

BOOTSTRAP_SERVERS = 'localhost:9092'

def create_topic_if_not_exists(topic_name, num_partitions=1, replication_factor=1):
    admin_client = AdminClient({'bootstrap.servers': BOOTSTRAP_SERVERS})
    metadata = admin_client.list_topics(timeout=10)
    if topic_name in metadata.topics:
        print(f"Topic '{topic_name}' already exists.")
        return

    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    futures = admin_client.create_topics([new_topic])

    for topic, future in futures.items():
        try:
            future.result()
            print(f"Topic '{topic}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic {topic}: {e}")

def produce_message(topic_name, message):
    create_topic_if_not_exists(topic_name)
    p = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

    def delivery_report(err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    p.produce(topic_name, json.dumps(message).encode('utf-8'), callback=delivery_report)
    p.flush()
