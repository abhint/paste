import os
from typing import Union
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv

load_dotenv()


def get_env(name: Union[URL, str]) -> Union[URL, str]:
    if name in os.environ:
        return os.environ[name]



