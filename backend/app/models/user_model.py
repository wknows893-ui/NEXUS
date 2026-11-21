from app.core.base import Base
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,DateTime
from datetime import datetime,UTC
from typing import Optional

class User(Base) :

    __tablename__ = "users"
    name : Mapped[str] = mapped_column(String(50))

    id : Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False
    )

    email : Mapped[str] = mapped_column(
        unique = True,
        nullable=False
    )

    password_hash  : Mapped[str] = mapped_column(
        nullable= False
    )

    status : Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True
    )

    created_at : Mapped[datetime]  = mapped_column(
        DateTime(timezone = True),
        default = lambda : datetime.now(UTC)
    )

    updated_at : Mapped[datetime]  = mapped_column(
            DateTime(timezone = True),
            default = lambda : datetime.now(UTC),
            onupdate = lambda : datetime.now(UTC)
    )

    last_login : Mapped[Optional[datetime]] 

    avatar_url : Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable = True
    )