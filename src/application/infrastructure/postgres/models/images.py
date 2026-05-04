from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from infrastructure.postgres.database import Base

class Image(Base):
    __tablename__ = "image"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)  # 'post', 'comment'
    object_id: Mapped[int] = mapped_column(nullable=False)  # id поста или комментария
    order: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)