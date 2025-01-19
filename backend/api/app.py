from flask import Flask
from flask_restful import Api, Resource
import psycopg

app = Flask(__name__)
api = Api(app)

class Test(Resource):
    def get(self):
        return {"data": "<div>Test</div>"}

api.add_resource(Test, "/test")

if __name__ == "__main__":
    app.run(debug=True)