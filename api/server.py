from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from api.database import engine

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
