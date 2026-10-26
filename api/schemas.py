from datetime import date
from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(RoleCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserCreate(BaseModel):
    full_name: str
    username: str
    role_id: int


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    username: str
    role_id: int
    is_active: bool


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "new"
    start_date: date | None = None
    end_date: date | None = None
    manager_id: int


class ProjectResponse(ProjectCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    manager_id: int | None = None


from decimal import Decimal


class StageCreate(BaseModel):
    project_id: int
    name: str
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str = "new"
    sort_order: int = 0


class StageUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None
    sort_order: int | None = None


class StageResponse(StageCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    stage_id: int | None = None
    assignee_id: int | None = None
    created_by: int
    priority: str = "medium"
    status: str = "new"
    due_date: date | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    stage_id: int | None = None
    assignee_id: int | None = None
    priority: str | None = None
    status: str | None = None
    due_date: date | None = None


class TaskResponse(TaskCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ---------- Сметы ----------

class EstimateCreate(BaseModel):
    project_id: int
    name: str
    description: str | None = None
    status: str = "draft"
    created_by: int


class EstimateResponse(EstimateCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EstimateItemCreate(BaseModel):
    item_type: str
    name: str
    description: str | None = None
    unit: str
    quantity: Decimal
    unit_price: Decimal


class EstimateItemResponse(EstimateItemCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    estimate_id: int
