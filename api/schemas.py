from datetime import date
from pydantic import BaseModel, ConfigDict


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
