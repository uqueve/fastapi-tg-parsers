import datetime as dt
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field
from enum import StrEnum, auto, unique
from utils.openai_service import OpenAIService
from utils.text_sevice import to_chunks


@unique
class SiteModel(StrEnum):
    URALSK = auto()
    EKATERINBURG = auto()
    ALMATA = auto()
    TASHKENT = auto()
    BAKU = auto()


class News(BaseModel):
    ids: list[str]


class PydanticObjectId(ObjectId):
    """
    ObjectId field. Compatible with Pydantic.
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, c):
        return PydanticObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: dict, c=None):
        field_schema.update(
            type="string",
            examples=["5eb7cf5a86d9755df3a6c593", "5eb7cfb05e32e07750a1756a"],
        )


class Post(BaseModel):
    id: Optional[PydanticObjectId] | str | None = Field(None, alias='_id')
    title: str | None = Field(default='')
    body: str | None = Field(default='')
    image_links: List[str] | None = Field(default=[])
    date: dt.datetime | None = Field(default=dt.datetime.now())
    link: str | None = Field(default='')
    city: SiteModel | None = Field(default=None)
    parser_name: str = Field(default='')
    posted: bool = Field(default=False)
    sent: bool = Field(default=False)

    def __str__(self):
        links = ''
        if self.image_links and None not in self.image_links:
            links = '\n'.join(self.image_links)

        return f'{self.title}\n\n{self.body}\n\nlinks:\n{links}\n{self.date}'

    def get_text(self):
        result = f'{self.title}\n\n{self.body}'
        return result

    def get_title(self):
        return self.title.capitalize()

    def get_body(self):
        return self.body

    def get_link(self, index):
        return self.image_links[index]

    def get_links(self):
        return self.image_links

    def images_count(self):
        return len(self.image_links)

    def get_date(self):
        return self.date


class PostOut(BaseModel):
    id: str = Field(alias='_id')
    title: str | None = Field(default='')
    body: str | None = Field(default='')
    image_links: List[str] | None = Field(default=[])
    date: str | None = Field(default='')
    link: str | None = Field(default='')
    city: SiteModel | None = Field(default=None)
    parser_name: str = Field(default='')
    posted: bool = Field(default=False)
    sent: bool = Field(default=False)


class CustomMediaChunks:
    def __init__(self, post: Post, translate: bool, convert_with_ai: bool):
        self.post = post
        self.title = post.title
        self.text = post.get_body()

        ai_service = OpenAIService()

        if translate:
            self.title = ai_service.translate_title_request(self.title)

        if convert_with_ai:
            self.text = ai_service.make_request(self.text)

        have_post = post.images_count() > 0
        self.media = None
        self.chunks = to_chunks(self.title, self.text, first_size=4096, other_size=4096)

        if have_post:
            self.media = []

            for i in range(min(post.images_count(), 10)):
                try:
                    self.media.append(dict(type='photo', media=post.get_link(i)))
                    self.media[0]['caption'] = post.get_text()
                except Exception as e:
                    pass

    def get_media(self):
        return self.media

    def get_text_chunks(self):
        return self.chunks

    def get_link(self):
        if self.post.images_count() > 0:
            return self.post.get_link(0)
        else:
            return "https://img.freepik.com/free-vector/oops-404-error-with-a-broken-robot-concept-illustration_114360-5529.jpg?w=740&t=st=1708030076~exp=1708030676~hmac=869cd3aa77fc267417e08a332b3d9771539014d7879bc848221bb191b5d7dc53"
