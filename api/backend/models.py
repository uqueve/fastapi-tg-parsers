from pydantic import BaseModel


class News(BaseModel):
    ids: list[str]


class Cities(BaseModel):
    oid: str
    name: str
    ru: str


class ErrorSchema(BaseModel):
    error: str
