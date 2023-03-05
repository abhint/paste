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


@app.route('/about')
def about_():
    return render_template("about.html")



@app.route('/<key>')
def view_(key: str):
    print(key)
    return render_template("index.html")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
