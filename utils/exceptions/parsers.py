from dataclasses import dataclass


@dataclass(eq=False)
class ParserError(Exception):
    @property
    def message(self) -> str:
        return 'Произошла ошибка парсера'
