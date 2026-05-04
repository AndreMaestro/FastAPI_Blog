from typing import List

from infrastructure.postgres.database import database
from infrastructure.postgres.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema


class GetAllPostsUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, limit: int = 100, offset: int = 0) -> List[PostResponseSchema]:
        async with self._database.session() as session:
            posts = await self._repo.get_all(session=session, limit=limit, offset=offset)
        return [PostResponseSchema.model_validate(obj=post) for post in posts]