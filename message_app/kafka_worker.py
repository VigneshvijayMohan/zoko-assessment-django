from confluent_kafka import Consumer, KafkaException
import time
from .models import Message
from .serializers import MessageSerializers
import json
 
import logging
logger = logging.getLogger(__name__)
 
BOOTSTRAP_SERVERS = 'localhost:9092'
 
 
def consume_messages(topic_name, group_id, timeout=5):
    c = Consumer({
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })

    c.subscribe([topic_name])
    logger.info(f"Consuming from topic '{topic_name}'...\n")

    messages = []

    try:
        start_time = time.time()
        while time.time() - start_time < timeout:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())

            decoded_message = msg.value().decode('utf-8')
            messages.append({
                'topic': msg.topic(),
                'partition': msg.partition(),
                'offset': msg.offset(),
                'key': msg.key().decode('utf-8') if msg.key() else None,
                'value': decoded_message,
                'timestamp': msg.timestamp()
            })

            logger.info(f"Received: {decoded_message} from {msg.topic()} [{msg.partition()}]")
            
    finally:
        c.close()
    data = json.loads(decoded_message)
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    content = data['content']
    message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )

    serialized = MessageSerializers(message)
    logger.info("Data is successfully added into the database")
    return serialized
