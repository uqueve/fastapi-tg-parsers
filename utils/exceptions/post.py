from dataclasses import dataclass


@dataclass(eq=False)
class PostValidateError(Exception):
    link: str | None = None

    @property
    def message(self) -> str:
        return 'Произошла ошибка валидации поста'


@dataclass
class PostNoTitleError(PostValidateError):
    @property
    def message(self) -> str:
        return f'Нет заголовка в новости. URL: {self.link}'


@dataclass
class PostNoBodyError(PostValidateError):
    @property
    def message(self) -> str:
        return f'Нет тела новости. URL: {self.link}'
