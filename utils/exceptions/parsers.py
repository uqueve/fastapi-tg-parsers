import json
from dataclasses import dataclass

from bs4 import BeautifulSoup

from utils.models import SiteModel


@dataclass(eq=False)
class ParserError(Exception):
    parser_name: str
    city: str

    @property
    def message(self) -> str:
        return 'Произошла ошибка парсера'


@dataclass(eq=False)
class ParserNoUrlsError(ParserError):
    source: BeautifulSoup | dict

    @property
    def message(self) -> str:
        return (f'Не удалось спарсить ссылки на новости. '
                f'Имя: {self.parser_name}. Город: {self.city}. Source: {self.source}')
