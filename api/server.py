import logging
logger = logging.getLogger(__name__)

from sqlalchemy.exc import IntegrityError
from api.models import Role, User
from api.schemas import (
    RoleCreate,
    RoleResponse,
    UserCreate,
    UserResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
    StageCreate,
    StageUpdate,
    StageResponse,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    EstimateCreate,
    EstimateResponse,
    EstimateItemCreate,
    EstimateItemResponse,
)
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError
from api.database import engine, SessionLocal
from api.models import (
    Role,
    User,
    Project,
    ProjectStage,
    Task,
    Estimate,
    EstimateItem,
)


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


@app.get("/users", response_model=list[UserResponse])
def get_users():
    db = SessionLocal()

    try:
        users = db.scalars(select(User)).all()
        return users

    except SQLAlchemyError:
        logger.exception("Ошибка при получении пользователей")
        raise HTTPException(
            status_code=500,
            detail="Failed to get users"
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


@app.get("/projects/{project_id}/stages",
         response_model=list[StageResponse])
def get_stages(project_id: int):
    db = SessionLocal()
    try:
        if db.get(Project, project_id) is None:
            raise HTTPException(404, "Project not found")

        return db.scalars(
            select(ProjectStage)
            .where(ProjectStage.project_id == project_id)
            .order_by(ProjectStage.sort_order, ProjectStage.id)
        ).all()
    finally:
        db.close()


@app.post("/stages", response_model=StageResponse, status_code=201)
def create_stage(data: StageCreate):
    db = SessionLocal()
    try:
        if db.get(Project, data.project_id) is None:
            raise HTTPException(404, "Project not found")

        stage = ProjectStage(**data.model_dump())
        db.add(stage)
        db.commit()
        db.refresh(stage)
        return stage
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка создания этапа")
        raise HTTPException(400, "Не удалось создать этап")
    finally:
        db.close()


@app.patch("/stages/{stage_id}", response_model=StageResponse)
def update_stage(stage_id: int, data: StageUpdate):
    db = SessionLocal()
    try:
        stage = db.get(ProjectStage, stage_id)
        if stage is None:
            raise HTTPException(404, "Stage not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(stage, key, value)

        db.commit()
        db.refresh(stage)
        return stage
    except HTTPException:
        raise
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка обновления этапа")
        raise HTTPException(400, "Не удалось обновить этап")
    finally:
        db.close()


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(stage_id: int | None = None,
              status: str | None = None):
    db = SessionLocal()
    try:
        query = select(Task)

        if stage_id is not None:
            query = query.where(Task.stage_id == stage_id)
        if status is not None:
            query = query.where(Task.status == status)

        return db.scalars(query.order_by(Task.id.desc())).all()
    finally:
        db.close()


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate):
    db = SessionLocal()
    try:
        task = Task(**data.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            400, "Проверь stage_id, assignee_id и created_by"
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка создания задачи")
        raise HTTPException(500, "Failed to create task")
    finally:
        db.close()


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate):
    db = SessionLocal()
    try:
        task = db.get(Task, task_id)
        if task is None:
            raise HTTPException(404, "Task not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)
        return task
    except HTTPException:
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Проверь связанные записи и значения")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка обновления задачи")
        raise HTTPException(500, "Failed to update task")
    finally:
        db.close()

@app.get("/estimates", response_model=list[EstimateResponse])
def get_estimates(project_id: int | None = None):
    db = SessionLocal()
    try:
        query = select(Estimate)

        if project_id is not None:
            query = query.where(Estimate.project_id == project_id)

        return db.scalars(query.order_by(Estimate.id.desc())).all()
    finally:
        db.close()


@app.post(
    "/estimates",
    response_model=EstimateResponse,
    status_code=201
)
def create_estimate(data: EstimateCreate):
    db = SessionLocal()
    try:
        if db.get(Project, data.project_id) is None:
            raise HTTPException(404, "Project not found")

        if db.get(User, data.created_by) is None:
            raise HTTPException(404, "User not found")

        estimate = Estimate(**data.model_dump())
        db.add(estimate)
        db.commit()
        db.refresh(estimate)
        return estimate

    except HTTPException:
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Проверьте данные сметы")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка создания сметы")
        raise HTTPException(500, "Failed to create estimate")
    finally:
        db.close()


@app.get(
    "/estimates/{estimate_id}/items",
    response_model=list[EstimateItemResponse]
)
def get_estimate_items(estimate_id: int):
    db = SessionLocal()
    try:
        if db.get(Estimate, estimate_id) is None:
            raise HTTPException(404, "Estimate not found")

        query = (
            select(EstimateItem)
            .where(EstimateItem.estimate_id == estimate_id)
            .order_by(EstimateItem.id)
        )
        return db.scalars(query).all()
    finally:
        db.close()


@app.post(
    "/estimates/{estimate_id}/items",
    response_model=EstimateItemResponse,
    status_code=201
)
def add_estimate_item(
    estimate_id: int,
    data: EstimateItemCreate
):
    db = SessionLocal()
    try:
        if db.get(Estimate, estimate_id) is None:
            raise HTTPException(404, "Estimate not found")

        item = EstimateItem(
            estimate_id=estimate_id,
            **data.model_dump()
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    except HTTPException:
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            400,
            "Проверьте тип позиции, количество и цену"
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Ошибка добавления позиции сметы")
        raise HTTPException(500, "Failed to add estimate item")
    finally:
        db.close()


@app.get("/estimates/{estimate_id}/total")
def get_estimate_total(estimate_id: int):
    db = SessionLocal()
    try:
        if db.get(Estimate, estimate_id) is None:
            raise HTTPException(404, "Estimate not found")

        items = db.scalars(
            select(EstimateItem).where(
                EstimateItem.estimate_id == estimate_id
            )
        ).all()

        works_total = sum(
            item.quantity * item.unit_price
            for item in items
            if item.item_type == "work"
        )

        materials_total = sum(
            item.quantity * item.unit_price
            for item in items
            if item.item_type == "material"
        )

        return {
            "estimate_id": estimate_id,
            "items_count": len(items),
            "works_total": works_total,
            "materials_total": materials_total,
            "grand_total": works_total + materials_total
        }
    finally:
        db.close()