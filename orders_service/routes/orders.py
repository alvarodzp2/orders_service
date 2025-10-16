from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
import os
import json
import pika
from dotenv import load_dotenv
from config.rabbit import get_connection

load_dotenv()

router = APIRouter()

# Conexión a MongoDB (Railway)
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["orders_db"]
orders_collection = db["orders"]

@router.post("/orders")
def crear_pedido(pedido: dict):
    try:
        # Guardar pedido en MongoDB
        result = orders_collection.insert_one(pedido)
        pedido_id = str(result.inserted_id)

        # Publicar mensaje en RabbitMQ
        try:
            connection, channel = get_connection()

            # Convertir pedido a un dict serializable (ObjectId → str)
            pedido_serializable = dict(pedido)
            pedido_serializable.pop("_id", None)  # eliminar _id si existe

            message = json.dumps({"order_id": pedido_id, **pedido_serializable})
            channel.basic_publish(
                exchange="",
                routing_key="orders_queue",
                body=message,
                properties=pika.BasicProperties(delivery_mode=2),  # mensaje persistente
            )
            connection.close()
            print(f"[x] Mensaje enviado a RabbitMQ: {message}")

        except Exception as mq_error:
            print(f"Error al publicar en RabbitMQ: {mq_error}")

        return {"mensaje": "Pedido creado", "order_id": pedido_id}

    except Exception as e:
        print(f"Error al crear pedido: {e}")
        raise HTTPException(status_code=500, detail=str(e))
