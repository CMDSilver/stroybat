import os
import secrets

from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from api.database import engine, Base
from api import models

app = FastAPI(title="Stroybat API")


@app.get("/")
def home():
    return {"message": "Stroybat API работает!"}


@app.get("/status")
def status():
    return {"status": "ok"}


@app.get("/db-check")
def db_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected"
        }

    except SQLAlchemyError:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )


@app.post("/init-db")
def init_db(key: str):
    secret_key = os.getenv("INIT_DB_SECRET")

    if not secret_key or not secrets.compare_digest(key, secret_key):
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    try:
        Base.metadata.create_all(bind=engine)
        return {"status": "ok", "message": "Таблицы созданы"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database initialization failed"
        )
