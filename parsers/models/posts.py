import datetime as dt
from uuid import uuid4

from pydantic import BaseModel, Field

from parsers.models.cities import CitySchema
from utils.blacklist import blackword_in_news_validate
from utils.exceptions.post import PostBlackWordInNewError, PostNoBodyError, PostNoTitleError


class Post(BaseModel):
    oid: str | None = Field(default_factory=uuid4)
    title: str | None = Field(default='')
    body: str | None = Field(default='')
    image_links: list[str] | None = Field(default_factory=list)
    date: dt.datetime | None = Field(default_factory=dt.datetime.now)
    link: str | None = Field(default=None)
    city: CitySchema | None = Field(default=None)
    parser_name: str = Field(default='')
    posted: bool = Field(default=False)
    sent: bool = Field(default=False)

    def model_post_init(self, __context) -> None:
        self.oid = str(self.oid)

    def __str__(self):
        links = ''
        if self.image_links and None not in self.image_links:
            links = '\n'.join(self.image_links)

        return f'{self.title}\n\n{self.body}\n\nlinks:\n{links}\n{self.date}'

    def post_validate(self) -> None:
        if not self.title:
            raise PostNoTitleError(link=self.link)
        if not self.body:
            raise PostNoBodyError(link=self.link)
        validate_blacklist_answer = blackword_in_news_validate(self.title)
        if not validate_blacklist_answer['ok']:
            raise PostBlackWordInNewError(word=validate_blacklist_answer['word'], link=self.link)
        validate_blacklist_answer = blackword_in_news_validate(self.body)
        if not validate_blacklist_answer['ok']:
            raise PostBlackWordInNewError(word=validate_blacklist_answer['word'], link=self.link)

    def get_text(self) -> str:
        result = f'{self.title}\n\n{self.body}'
        return result

    def get_title(self) -> str:
        return self.title.capitalize()

    def get_body(self) -> str:
        return self.body

    def get_link(self, index: int) -> str:
        return self.image_links[index]

    def get_links(self) -> list[str]:
        return self.image_links

    def images_count(self) -> int:
        return len(self.image_links)

    def get_date(self) -> dt.datetime:
        return self.date


class PostOut(BaseModel):
    oid: str = Field(alias='oid')
    title: str | None = Field(default='')
    body: str | None = Field(default='')
    image_links: list[str] | None = Field(default=[])
    date: str | None = Field(default='')
    link: str | None = Field(default='')
    city: CitySchema = Field(alias='city')
    parser_name: str = Field(default='')
    posted: bool = Field(default=False)
    sent: bool = Field(default=False)
