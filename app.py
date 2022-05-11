# config
from config import PATH_DB

# models
from models import City

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class CityList(Resource):
    def __init__(self):
        Session = sessionmaker(bind=create_engine(PATH_DB, echo=False))
        self.s = Session()

    def get(self):
        data = self.s.query(City).all()
        return {'cities': list(x.json() for x in data)}


@app.route('/')
def index():
    return "<h1>Hello, world!</h1>"

api.add_resource(CityList, '/1')

if __name__ == '__main__':
    app.run(debug=True)