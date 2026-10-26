from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.database import Base

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(Text)

    users: Mapped[list["User"]] = relationship(back_populates="role")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    role: Mapped["Role"] = relationship(back_populates="users")

    managed_projects: Mapped[list["Project"]] = relationship(
        back_populates="manager",
        foreign_keys="Project.manager_id",
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="assignee",
        foreign_keys="Task.assignee_id",
    )
    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="creator",
        foreign_keys="Task.created_by",
    )
    created_estimates: Mapped[list["Estimate"]] = relationship(
        back_populates="creator",
        foreign_keys="Estimate.created_by",
    )

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(30), default="new", nullable=False
    )
    start_date: Mapped[Date | None] = mapped_column(Date)
    end_date: Mapped[Date | None] = mapped_column(Date)
    manager_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR start_date IS NULL "
            "OR end_date >= start_date",
            name="ck_projects_dates",
        ),
        CheckConstraint(
            "status IN ('new', 'in_progress', 'on_hold', 'completed')",
            name="ck_projects_status",
        ),
    )

    manager: Mapped["User"] = relationship(
        back_populates="managed_projects",
        foreign_keys=[manager_id],
    )
    stages: Mapped[list["ProjectStage"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    estimates: Mapped[list["Estimate"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )

class ProjectStage(Base):
    __tablename__ = "project_stages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    start_date: Mapped[Date | None] = mapped_column(Date)
    end_date: Mapped[Date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(
        String(30), default="new", nullable=False
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "end_date IS NULL OR start_date IS NULL "
            "OR end_date >= start_date",
            name="ck_project_stages_dates",
        ),
        CheckConstraint(
            "status IN ('new', 'in_progress', 'completed')",
            name="ck_project_stages_status",
        ),
    )

    project: Mapped["Project"] = relationship(back_populates="stages")
    tasks: Mapped[list["Task"]] = relationship(back_populates="stage")

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    stage_id: Mapped[int | None] = mapped_column(
        ForeignKey("project_stages.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    priority: Mapped[str] = mapped_column(
        String(20), default="medium", nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(30), default="new", nullable=False
    )
    due_date: Mapped[Date | None] = mapped_column(Date)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high')",
            name="ck_tasks_priority",
        ),
        CheckConstraint(
            "status IN ('new', 'in_progress', 'review', 'completed')",
            name="ck_tasks_status",
        ),
    )

    stage: Mapped["ProjectStage | None"] = relationship(
        back_populates="tasks"
    )
    assignee: Mapped["User | None"] = relationship(
        back_populates="assigned_tasks",
        foreign_keys=[assignee_id],
    )
    creator: Mapped["User"] = relationship(
        back_populates="created_tasks",
        foreign_keys=[created_by],
    )

class Estimate(Base):
    __tablename__ = "estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        String(30), default="draft", nullable=False
    )
    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'approved', 'archived')",
            name="ck_estimates_status",
        ),
    )

    project: Mapped["Project"] = relationship(
        back_populates="estimates"
    )
    creator: Mapped["User"] = relationship(
        back_populates="created_estimates"
    )
    items: Mapped[list["EstimateItem"]] = relationship(
        back_populates="estimate",
        cascade="all, delete-orphan",
    )

class EstimateItem(Base):
    __tablename__ = "estimate_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estimate_id: Mapped[int] = mapped_column(
        ForeignKey("estimates.id"), nullable=False
    )
    item_type: Mapped[str] = mapped_column(
        String(20), nullable=False
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    quantity: Mapped[float] = mapped_column(
        Numeric(12, 3), nullable=False
    )
    unit_price: Mapped[float] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "item_type IN ('work', 'material')",
            name="ck_estimate_items_type",
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_estimate_items_quantity",
        ),
        CheckConstraint(
            "unit_price >= 0",
            name="ck_estimate_items_price",
        ),
    )

    estimate: Mapped["Estimate"] = relationship(
        back_populates="items"
    )
