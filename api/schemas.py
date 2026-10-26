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
