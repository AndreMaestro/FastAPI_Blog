class BaseDatabaseExceptions(Exception):
    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail


class UserNotFoundException(BaseDatabaseExceptions):
    pass


class UsernameAlreadyExistsException(BaseDatabaseExceptions):
    pass


class CategoryNotFoundException(BaseDatabaseExceptions):
    pass


class CategorySlugAlreadyExistsException(BaseDatabaseExceptions):
    pass


class CommentNotFoundException(BaseDatabaseExceptions):
    pass


class PostNotFoundException(BaseDatabaseExceptions):
    pass


class LocationNotFoundException(BaseDatabaseExceptions):
    pass


class LocationNameAlreadyExistsException(BaseDatabaseExceptions):
    pass
