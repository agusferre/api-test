from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class test(Resource):
    def get(self):
        return {'data': 'hey dog'}

    def post(self):
        return {'data': 'heya'}

api.add_resource(test, '/doggy')

if __name__ == '__main__':
    app.run(debug=True)