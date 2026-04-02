from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.sqlite.database import Base


class User(Base):
    __tablename__ = 'auth_user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(nullable=True)
    is_superuser: Mapped[bool] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    is_staff: Mapped[bool] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(nullable=False)
    date_joined: Mapped[datetime] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author")