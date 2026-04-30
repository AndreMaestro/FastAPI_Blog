from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from infrastructure.sqlite.database import Base


class Post(Base):
    __tablename__ = 'blog_post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_published: Mapped[bool] = mapped_column(nullable=False)
    title: Mapped[str] =  mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("blog_category.id"), nullable=True)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("blog_location.id"), nullable=True)
    image: Mapped[str] = mapped_column(nullable=True, default="")
    pub_date: Mapped[datetime] = mapped_column(nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    category: Mapped["Category | None"] = relationship(back_populates="posts")
    location: Mapped["Location | None"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan",
        passive_deletes=True
    )