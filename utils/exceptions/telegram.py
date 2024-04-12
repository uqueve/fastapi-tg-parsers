from dataclasses import dataclass


@dataclass(eq=False)
class TelegramSendException(Exception):
    @property
    def message(self):
        return 'Произошла ошибка при отправке новости'