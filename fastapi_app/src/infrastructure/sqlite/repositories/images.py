from typing import Literal, List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.exceptions.database_exceptions import ImageNotFoundException
from infrastructure.sqlite.models.images import Image
from infrastructure.sqlite.repositories.base import BaseRepository

ContentType = Literal['post', 'comment']

class ImageRepository(BaseRepository[Image]):
    def __init__(self):
        super().__init__(Image, ImageNotFoundException)

    def add_images(self, session: Session, content_type: ContentType,
            object_id: int, file_path: List[str]) -> List[Image]:

        images = []
        for order, path in enumerate(file_path):
            image = Image(
                file_path=path,
                content_type=content_type,
                object_id=object_id,
                order=order
            )
            session.add(image)
            images.append(image)
        session.flush()
        return images

    def get_images(
            self,
            session: Session,
            content_type: ContentType,
            object_id: int
    ) -> List[Image]:
        return session.query(Image).filter(
            Image.content_type==content_type, Image.object_id==object_id
        ).order_by(Image.order).all()


    def delete_images(
            self,
            session: Session,
            content_type: ContentType,
            object_id: int
    ):
        session.query(Image).filter(
            Image.content_type==content_type, Image.object_id==object_id
        ).delete()