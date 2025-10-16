import pika
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
    channel = connection.channel()
    channel.queue_declare(queue="orders_queue", durable=True)
    return connection, channel
