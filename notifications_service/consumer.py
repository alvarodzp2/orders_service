import json
import time
from config.rabbit import get_connection

def callback(ch, method, properties, body):
    try:
        mensaje = json.loads(body)
        pedido_id = mensaje.get("order_id")
        print(f"Nuevo pedido recibido: {pedido_id}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print("Error procesando mensaje:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag)

def start_consumer():
    while True:
        try:
            connection, channel = get_connection()
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue="orders_queue", on_message_callback=callback)
            print("Esperando nuevos pedidos...")
            channel.start_consuming()
        except Exception as e:
            print("Error en la conexión, reintentando en 5s:", e)
            time.sleep(5)

if __name__ == "__main__":
    start_consumer()
