#!/usr/bin/env python3
# from shortuuid.django_fields import ShortUUIDField
import re
from shortuuid import ShortUUID
from datetime import datetime
from typing import Optional, Union
from sqlalchemy.engine.url import URL
from sqlmodel import Field, Session, SQLModel, create_engine, select


class DataBase(SQLModel, table=True):
    __tablename__: str = 'past'
    id: Optional[int] = Field(primary_key=True)
    key: Optional[str]
    title: Optional[str]
    author: Optional[str] = None
    date: str = datetime.now()
    views: Optional[int] = 0
    length: int
    language: Optional[str] = 'plaintext'
    content: str


class Past:
    def __init__(self,
                 url: Union[str, URL]):
        self.url = url
        self.engine = create_engine(url=self.url)
        SQLModel.metadata.create_all(self.engine)

    @staticmethod
    def keyGenerator(content: str):
        character = re.search(r"^[a-zA-Z0-9 ]*$", content)
        key = ShortUUID(character).random(8)
        return key

    def sanitize(self, content: any) -> dict:
        self.add(DataBase(
            key=self.keyGenerator(content["content"]),
            length=len(content["content"]),
            content=content["content"])
        )
        return content

    def add(self, db: DataBase):
        with Session(self.engine) as session:
            session.add(db)
            session.commit()

