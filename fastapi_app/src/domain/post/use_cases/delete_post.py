from infrastructure.sqlite.database import database
from infrastructure.sqlite.repositories.posts import PostRepository


class DeletePostUseCase:
    def __init__(self):
        self._database = database
        self._repo = PostRepository()

    async def execute(self, post_id: int) -> bool:
        with self._database.session() as session:
            self._repo.delete(session=session, id=post_id)

        return True