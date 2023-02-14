from flask_restful import Api
from until import APIHandling, View
from flask import Flask, render_template

app = Flask(__name__)
api = Api(app=app)

api.add_resource(APIHandling, '/api')
api.add_resource(View, '/api/p/<key>')


@app.errorhandler(404)
def err_(e):
    return render_template("index.html"), 404


@app.route('/<key>')
def view_(key: str):
    print(key)
    return render_template("index.html")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=4000, host="0.0.0.0")
