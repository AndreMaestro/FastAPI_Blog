from datetime import datetime

from fastapi import HTTPException, status

from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from schemas.posts import PostResponseSchema, PostCreateSchema


class CreatePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, dto: PostCreateSchema) -> PostResponseSchema:
        with self._database.session() as session:
            post = self._repo.create(
                session=session,
                title=dto.title,
                text=dto.text,
                is_published=dto.is_published,
                created_at=datetime.now(),
                pub_date=dto.pub_date,
                author_id=dto.author_id,
                category_id=dto.category_id,
                location_id=dto.location_id,
                image=dto.image or '',
            )
            session.flush()
            post_with_relations = self._repo.get_by_id_with_relations(
                session=session, post_id=post.id
            )

        if post_with_relations is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Created post could not be loaded',
            )

        missing_relations = []
        if post_with_relations.author is None:
            missing_relations.append(f"author_id={dto.author_id}")
        if post_with_relations.location is None:
            missing_relations.append(f"location_id={dto.location_id}")
        if post_with_relations.category is None:
            missing_relations.append(f"category_id={dto.category_id}")

        if missing_relations:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Related entities not found: {', '.join(missing_relations)}",
            )

        return PostResponseSchema.model_validate(obj=post_with_relations)