class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с юзернеймом {username} не найден"

    def __init__(self, username : str) -> None:
        self._exception_text_template = self._exception_text_template.format(username=username)

        super().__init__(detail=self._exception_text_template)


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с ID = {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class UserIsNotUniqueByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с username = {usename} уже зарегистрирован"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(username=username)

        super().__init__(detail=self._exception_text_template)


class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с ID = {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Локация с ID = {id} не найдена"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class LocationNameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Локация '{name}' уже существует"

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(name=name)

        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с ID = {id} не найден"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с ID = {id} не найдена"

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория с slug = '{slug}' не найдена"

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)

        super().__init__(detail=self._exception_text_template)


class CategorySlugIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория с slug = '{slug}' уже существует"

    def __init__(self, slug: str):
        self._exception_text_template = self._exception_text_template.format(slug=slug)

        super().__init__(detail=self._exception_text_template)