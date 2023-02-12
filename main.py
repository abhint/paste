from flask_restful import Api
from until import APIHandling
from flask import Flask, render_template

app = Flask(__name__)
api = Api(app=app)


api.add_resource(APIHandling, '/api')


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=4000, host="0.0.0.0")
