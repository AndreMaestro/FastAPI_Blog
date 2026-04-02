from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema, PostUpdateSchema


class UpdatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int, dto: PostUpdateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.update(
                session=session,
                id=post_id,
                title=dto.title,
                text=dto.text,
                is_published=dto.is_published,
                category_id=dto.category_id,
                location_id=dto.location_id,
            )

            if post is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Post with id {post_id} not found',
                )

            post_with_relations = self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)