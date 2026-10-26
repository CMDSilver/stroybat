import logging
logger = logging.getLogger(__name__)

from sqlalchemy.exc import IntegrityError
from api.models import Role, User
from api.schemas import RoleCreate, RoleResponse, UserCreate, UserResponse
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from api.schemas import ProjectUpdate
from api.database import engine, SessionLocal
from api.models import Project
from api.schemas import ProjectResponse, ProjectCreate


app = FastAPI(title="Stroybat API")

@app.post("/roles", response_model=RoleResponse, status_code=201)
def create_role(role_data: RoleCreate):
    db = SessionLocal()

    try:
        role = Role(**role_data.model_dump())

        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Роль с таким названием уже существует"
        )

    finally:
        db.close()

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate):
    db = SessionLocal()

    try:
        user = User(
            full_name=user_data.full_name,
            username=user_data.username,
            role_id=user_data.role_id,
            password_hash="demo-user-no-auth",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Пользователь уже существует или указана неверная роль"
        )

    finally:
        db.close()





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


@app.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(project_data: ProjectCreate):
    db = SessionLocal()

    try:
        project = Project(**project_data.model_dump())

        db.add(project)
        db.commit()
        db.refresh(project)

        return project

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Ошибка данных проекта. Проверь manager_id и даты."
        )

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка при создании проекта")
        raise HTTPException(
            status_code=500,
            detail="Failed to create project"
        )

    finally:
        db.close()


@app.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    db = SessionLocal()

    try:
        project = db.get(Project, project_id)

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        return project

    except SQLAlchemyError:
        logger.exception("Ошибка при получении проекта")
        raise HTTPException(
            status_code=500,
            detail="Failed to get project"
        )

    finally:
        db.close()


@app.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate):
    db = SessionLocal()

    try:
        project = db.get(Project, project_id)

        if project is None:
            raise HTTPException(
                status_code=404,
                detail="Project not found"
            )

        update_data = project_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(project, field, value)

        db.commit()
        db.refresh(project)

        return project

    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка при обновлении проекта")
        raise HTTPException(
            status_code=500,
            detail="Failed to update project"
        )

    finally:
        db.close()
