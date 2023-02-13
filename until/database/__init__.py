from .database import Past, DataBase


class DB(Past):
    def __init__(self):
        super().__init__(url="sqlite:///HelloDB.db")
