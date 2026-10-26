import logging
logger = logging.getLogger(__name__)


from fastapi import FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError

from api.database import engine, SessionLocal
from api.models import Project
from api.schemas import ProjectResponse


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


@app.get("/projects", response_model=list[ProjectResponse])
def get_projects():
    db = SessionLocal()

    try:
        projects = db.scalars(select(Project)).all()
        return projects


    except SQLAlchemyError:

        logger.exception("Ошибка при получении проектов")

        raise HTTPException(

            status_code=500,

            detail="Failed to get projects"

        )

    finally:
        db.close()
