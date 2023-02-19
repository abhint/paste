from .database import Past, DataBase
from config import get_env


class DB(Past):
    def __init__(self):
        super().__init__(url=get_env("DATABASE_URL"))
