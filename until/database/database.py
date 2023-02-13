#!/usr/bin/env python3

import re
# from config import BASE_URL
from shortuuid import ShortUUID
from datetime import datetime
from typing import Optional, Union
from sqlalchemy.engine.url import URL
from sqlmodel import Field, Session, SQLModel, create_engine, select, col


class DataBase(SQLModel, table=True):
    __tablename__: str = 'past'
    id: Optional[int] = Field(primary_key=True)
    key: str = Field(index=True)
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
        self.dataBase = DataBase
        SQLModel.metadata.create_all(self.engine)

    @staticmethod
    def keyGenerator(content: str) -> str:
        character = re.sub(r'[^\w]', '', content)  # https://stackoverflow.com/a/875978/11913751
        key = ShortUUID(character).random(8)
        return key

    def sanitize(self, content: any) -> dict:
        key_ = self.keyGenerator(content["content"])
        self.add(DataBase(
            key=key_,
            length=len(content["content"]),
            content=content["content"])
        )

        return key_

    def add(self, db: DataBase):
        with Session(self.engine) as session:
            session.add(db)
            session.commit()

    def selectContent(self, key: str):
        with Session(self.engine) as session:
            statement = select(self.dataBase).where(col(self.dataBase.key) == key)
            result = session.exec(statement).all()
            return result
