from app.core.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,ForeignKey,DateTime
from datetime import datetime,UTC

class Project(Base) :
    __tablename__ = "projects"
    id : Mapped[int] = mapped_column(
        primary_key= True
    )
    organization_id : Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable = False
    )
    name : Mapped[str] = mapped_column(
        String(50),
        nullable = False
    )
    description : Mapped[str] = mapped_column(
        String(120),
        nullable = False
    )
    status : Mapped[str] = mapped_column(
        String,
        nullable = False
    )
    owner_id : Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable = False
    )
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default = lambda : datetime.now(UTC)
    )
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone = True),
        default = lambda : datetime.now(UTC),
        onupdate= datetime.now(UTC)
    )
    deadline : Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )