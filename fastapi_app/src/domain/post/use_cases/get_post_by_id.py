from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema


class GetPostByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.get_by_id_with_relations(session=session, post_id=post_id)

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Post with id {post_id} not found',
            )

        return PostResponseSchema.model_validate(obj=post)