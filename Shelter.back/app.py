from flask import Flask, render_template, request, redirect, url_for, jsonify, json
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_restful import reqparse, Resource, Api, fields, marshal_with
from flask_cors import CORS, cross_origin
import sys
from models import db, Element, Tag


app = Flask(__name__)

if app.config["ENV"] == "production":
  app.config.from_object("config.ProductionConfig")
else:
  app.config.from_object("config.DevelopmentConfig")

logging.basicConfig(
  format='%(asctime)s %(message)s',
  filename='shelter.log',
  level=logging.INFO,
  datefmt='%m/%d/%Y %I:%M:%S %p')

db.init_app(app)

logging.info('app start')
print(f'ENV is set to: {app.config["ENV"]}')

api = Api(app)
cors = CORS(app)

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
  'tags': fields.List(fields.Nested(tag_fields), attribute='tags_associated')
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
    logging.info('input: {json}'.format(json= args))
    try:

      # TODO : code inadmissible :D
      already_existing_tags = Tag.query.filter(Tag.label.in_(args.tags or [])).all()
      already_existing_tags_labels = set(map(lambda t: t.label, already_existing_tags))
      received_tags = set(args.tags or [])
      new_tags = [Tag(t) for t in (received_tags - already_existing_tags_labels)]
      all_tags_to_add = set(new_tags) | set(already_existing_tags)
      new_element = Element(args['title'], args['text'], list(all_tags_to_add))

      db.session.add(new_element)
      db.session.commit()
      return new_element, 201
    except:
      print("Unexpected error:", sys.exc_info()[0])
      return 'Error', 400

api.add_resource(ElementsListApi, '/api/elements')
api.add_resource(ElementApi, '/api/elements/<element_id>')

if __name__ == '__main__':
  app.debug = True
  app.run()
  # app.run(host='0.0.0.0', port=4996)
