import pika
import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

RABBITMQ_URL = os.getenv("RABBITMQ_URL")

def get_connection():
    params = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue="orders_queue", durable=True)
    return connection, channel
