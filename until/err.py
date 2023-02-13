from werkzeug.exceptions import HTTPException


class Error(HTTPException):
    err400 = "Item Not found"

    def __init__(self, code, description):
        self.code = code
        self.description = description
        super().__init__(self.code, self.description)
