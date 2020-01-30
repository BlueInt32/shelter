from flask import Flask, render_template, request, redirect, url_for
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, fields, marshal_with
from flask_cors import CORS, cross_origin
from datetime import datetime
import sys

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
api = Api(app)
cors = CORS(app)

POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "Simon"
POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
POSTGRES_DB = "shelter"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)

parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('text')
parser.add_argument('tags', action='append')

tag_fields = {
    'id': fields.Integer,
    'label': fields.String
}
element_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    # 'creation_date': fields.DateTime,
    # 'update_date': fields.DateTime,
    'tags': fields.Nested(tag_fields)
}


class ElementApi(Resource):
    @marshal_with(element_fields)
    def get(self, element_id):
        retrieved_element = Element.query.get(element_id)
        return retrieved_element

    def put(self, element_title):
        args = parser.parse_args(strict=True)
        new_element = Element(args['title'].title)
        db.session.add(new_element)
        db.session.commit()
        return new_element, 201


class ElementsListApi(Resource):
    @marshal_with(element_fields)
    def get(self):
        # t.start('done and done')
        elements = db.session.query(Element).all()
        # t.stop('done and done')
        return elements

    @marshal_with(element_fields)
    def post(self):
        args = parser.parse_args()
        try:
            new_tags = [Tag(a) for a in args.tags or []]
            new_element = Element(args['title'], args['text'], new_tags)
            db.session.add(new_element)
            db.session.commit()
            return new_element.id, 201
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return 'Error', 400


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('element_id', db.Integer, db.ForeignKey('element.id'), primary_key=True),
                )


class Element(db.Model):
    def __init__(self, title, text, input_tags):
        self.title = title
        self.text = text
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
        self.tags_associated = input_tags

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    text = db.Column(db.String(200), unique=False, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)
    tags_associated = db.relationship('Tag', secondary=tags, lazy='subquery',
                                      backref=db.backref('elements_associated', lazy=True))

    # def __repr__(self):
    #     return '<Element %r>' % self.title


class Tag(db.Model):
    def __init__(self, label):
        self.label = label

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), unique=True, nullable=False)


api.add_resource(ElementsListApi, '/api/elements')
api.add_resource(ElementApi, '/api/elements/<element_id>')

if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=4996)
