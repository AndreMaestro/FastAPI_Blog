from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from infrastructure.sqlite.database import Base

class Comment(Base):
    __tablename__ = 'blog_comment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("auth_user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_post.id", ondelete="CASCADE"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")