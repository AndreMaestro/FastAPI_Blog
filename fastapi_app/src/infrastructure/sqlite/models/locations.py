from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from infrastructure.sqlite.database import Base


class Location(Base):
    __tablename__ = "blog_location"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="location")