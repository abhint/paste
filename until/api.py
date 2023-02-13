from flask import redirect
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
        super().__init__(url="sqlite:///abbb.db")

    def post(self):
        try:
            args = parser.parse_args()
            print(args)
        except HTTPException as err:
            error_message.update({"code": err.code})
            return abort(err.code, error_message)

        self.sanitize(args)
        return 0


    def get(self):
        return redirect("/")
