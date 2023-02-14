from flask import redirect, Response
from typing import Optional, Union
from .database import DB
from flask_restful import Resource, reqparse
from werkzeug.exceptions import HTTPException, abort

parser = reqparse.RequestParser(bundle_errors=True)
error_message = {"error": "Something is Wrong"}
parser.add_argument('content',
                    type=str,
                    required=True)


class APIHandling(DB, Resource):
    def __init__(self):
        super().__init__()

    def post(self) -> Optional[Union[dict, HTTPException]]:
        try:
            args = parser.parse_args()
        except HTTPException as err:
            error_message.update({"code": err.code})
            return abort(err.code, error_message)

        return {"key": self.sanitize(args)}

    def get(self) -> Response:
        return redirect("/")
