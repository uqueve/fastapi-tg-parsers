from dataclasses import dataclass


@dataclass(eq=False)
class ParserException(Exception):
    @property
    def message(self):
        return 'Произошла ошибка парсера'


