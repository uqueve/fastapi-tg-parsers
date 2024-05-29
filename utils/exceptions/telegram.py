from dataclasses import dataclass

from parsers.models.posts import Post


@dataclass
class TelegramSendError(Exception):
    @property
    def message(self) -> str:
        return 'Произошла ошибка при отправке новости'


@dataclass
class TelegramSendPhotoError(TelegramSendError):
    post: Post
    response: dict
    caption: str
    photo: str

    @property
    def message(self) -> str:
        return (
            f'Ошибка при отправке фото в канал. Парсер: {self.post.city.ru}\n'
            f'\nОтвет сервера: {self.response}\nФото для отправки: {self.photo}.Подпись: {self.caption}'
        )


@dataclass
class TelegramSendMediaGroupError(TelegramSendError):
    post: Post
    response: dict
    media: list[dict]

    @property
    def message(self) -> str:
        return (
            f'Ошибка при отправке сообщения в канал. Парсер: {self.post.city.ru}\n'
            f'\nОтвет сервера: {self.response}\nМедиа для отправки: {self.media}'
        )


@dataclass
class TelegramSendMessageError(TelegramSendError):
    post: Post
    response: dict
    tg_text: str

    @property
    def message(self) -> str:
        return (
            f'Ошибка при отправке сообщения в канал. Парсер: {self.post.city.ru}\n'
            f'\nОтвет сервера: {self.response}\nТекст для отправки: {self.tg_text}'
        )
