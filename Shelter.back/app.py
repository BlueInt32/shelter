from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, fields, marshal_with
from server_timing import Timing
from flask_cors import CORS, cross_origin
from flask_restful.utils import cors

app = Flask(__name__)
api = Api(app)
# api.decorators = [cors.crossdomain(origin='*')]
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# t = Timing(app, force_debug=True)
# app.config['CORS_HEADERS'] = 'Content-Type'

POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "Simon"
POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
POSTGRES_DB = "shelter"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shelter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)

parser = reqparse.RequestParser()
parser.add_argument('title')

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String
}


class ElementApi(Resource):
    @marshal_with(resource_fields)
    def get(self, element_id):
        retrieved_element = Element.query.get(element_id)
        return retrieved_element

    def put(self, element_title):
        args = parser.parse_args(strict=True)
        new_element = Element(title=args['title'].title)
        db.session.add(new_element)
        db.session.commit()
        return new_element, 201


class ElementsListApi(Resource):
    @marshal_with(resource_fields)
    def get(self):
        #t.start('done and done')
        elements = db.session.query(Element).all()
        #t.stop('done and done')
        return elements

    def post(self):
        args = parser.parse_args()
        new_element = Element(title=args['title'], description='le trombonne')
        db.session.add(new_element)
        db.session.commit()
        return new_element.id, 201


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)


api.add_resource(ElementsListApi, '/api/elements')
api.add_resource(ElementApi, '/api/elements/<element_id>')

# landing page that will display all the books in our database
# This function operate on the Read operation.
# @app.route('/')
# @app.route('/elements')
# def show_books():
#     print(__name__)
#     elements = db.session.query(Element).all()
#     return {'items': elements}
#
#
# # This will let us Create a new book and save it in our database
# @app.route('/elements', methods=['POST'])
# def create_new_element():
#     new_element = Element(title=request.form['title'], description=request.form['title'])
#     db.session.add(new_element)
#     db.session.commit()
#     return {'created': new_element}


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=4996)
