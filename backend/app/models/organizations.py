from app.core.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,DateTime
from datetime import datetime,UTC
from typing import Optional
class Organization(Base):

    __tablename__ = "organizations"
    id : Mapped[int] = mapped_column(
        primary_key=True,
        nullable= False
    )
    name : Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    slug : Mapped[str] = mapped_column(
        String(100)
    )
    description : Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True
    )
    owner_id : Mapped[int] = mapped_column(
        nullable=False
    )
    created_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default = lambda : datetime.now(UTC)
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default= lambda : datetime.now(UTC),
        onupdate=lambda : datetime.now(UTC)
    )