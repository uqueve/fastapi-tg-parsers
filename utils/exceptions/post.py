from dataclasses import dataclass


@dataclass(eq=False)
class PostValidateException(Exception):
    link: str | None = None

    @property
    def message(self):
        return 'Произошла ошибка валидации поста'


@dataclass
class PostNoTitleError(PostValidateException):

    @property
    def message(self):
        return f'Нет заголовка в новости. URL: {self.link}'


@dataclass
class PostNoBodyError(PostValidateException):

    @property
    def message(self):
        return f'Нет тела новости. URL: {self.link}'
    