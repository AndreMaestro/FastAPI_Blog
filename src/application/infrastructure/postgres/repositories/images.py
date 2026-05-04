from typing import Literal, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.exceptions.database_exceptions import ImageNotFoundException
from infrastructure.postgres.models.images import Image
from infrastructure.postgres.repositories.base import BaseRepository

ContentType = Literal['post', 'comment']

class ImageRepository(BaseRepository[Image]):
    def __init__(self):
        super().__init__(Image, ImageNotFoundException)

    async def add_images(self, session: AsyncSession, content_type: ContentType,
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
        await session.flush()
        return images

    async def get_images(
            self,
            session: AsyncSession,
            content_type: ContentType,
            object_id: int
    ) -> List[Image]:
        query = await session.execute(
            select(self._model)
            .where(Image.content_type==content_type, Image.object_id==object_id)
            .order_by(Image.order)
        )
        return list(query.scalars().all())


    async def delete_images(
            self,
            session: AsyncSession,
            content_type: ContentType,
            object_id: int
    ):
        await session.execute(
            delete(self._model)
            .where(Image.content_type==content_type, Image.object_id==object_id)
        )