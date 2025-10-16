from fastapi import FastAPI
from routes.orders import router as orders_router

app = FastAPI(title="Orders Service")

# Montar rutas
app.include_router(orders_router)
