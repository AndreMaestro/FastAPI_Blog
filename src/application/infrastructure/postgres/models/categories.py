from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.postgres.database import Base


class Category(Base):
    __tablename__ = 'blog_category'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    slug: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="category")