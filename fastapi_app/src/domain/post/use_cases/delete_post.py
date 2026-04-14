from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository
from core.exceptions.domain_exceptions import PostNotFoundByIdException
from core.exceptions.database_exceptions import PostNotFoundException


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> bool:
        try:
            with self._database.session() as session:
                self._repo.delete(session=session, id=post_id)
        except PostNotFoundException:
            raise PostNotFoundByIdException(id=post_id)

        return True