from .database import DB
from flask import redirect
from flask_restful import Resource, reqparse
from werkzeug.exceptions import abort
from .err import Error

parser = reqparse.RequestParser(bundle_errors=True)


class View(Resource, DB):
    def __init__(self):
        super().__init__()

    def post(self, key):
        try:
            return self.view_content(key)
        except Error as err:
            return abort(err.code, err.err400)

    def get(self, key):
        return redirect(f'/{key}')

    def view_content(self, key: str):
        result = self.selectContent(key)
        print(result)

    def view_content(self, key):
        database_ = self.selectContent(key)
        if not database_:
            raise Error(description="No Content", code=400)
        result = database_[0]
        return {
            "key": result.key,
            "content": result.content
        }
