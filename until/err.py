from typing import Optional
from werkzeug.exceptions import HTTPException


class Error(HTTPException):
    code: Optional[int] = None
    description: Optional[str] = None
    err400 = "Item Not found"

    def __init__(self,
                 code: Optional[int],
                 description: Optional[str]):
        self.code = code
        self.description = description
        super().__init__(self.code, self.description)
