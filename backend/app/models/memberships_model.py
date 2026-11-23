from app.core.base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey,String,DateTime,UniqueConstraint
from datetime import datetime,UTC
from typing import Optional
class Membership(Base):

    __tablename__ = "memberships"

    __table_args__ = (UniqueConstraint("user_id","organization_id"),)
    id : Mapped[int] = mapped_column(
        primary_key=True
    )
    user_id : Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    organization_id : Mapped[int] = mapped_column(
        ForeignKey("organizations.id") 
    )
    role : Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=False
    )
    joined_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default = lambda : datetime.now(UTC)
    )