from .database import DB
from typing import Optional, Union
from flask import redirect, Response
from flask_restful import Resource, reqparse
from werkzeug.exceptions import abort
from .err import Error

parser = reqparse.RequestParser(bundle_errors=True)


class View(Resource, DB):

    def post(self, key) -> Optional[Union[Error, dict]]:
        try:
            return self.view_content(key)
        except Error as err:
            return abort(err.code, err.err400)

    def get(self, key) -> Response:
        return redirect(f'/{key}', 404)


    def view_content(self, key) -> Optional[Union[dict,Error]]:
        database_ = self.selectContent(key)
        if not database_:
            raise Error(description="No Content", code=400)
        result = database_[0]
        return {
            "key": result.key,
            "content": result.content
        }
