# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.database.connection import Base, engine
from backend.routes import exchange, order, admin

# создаём таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title="GridEx Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(exchange.router)
app.include_router(order.router)
app.include_router(admin.router)
