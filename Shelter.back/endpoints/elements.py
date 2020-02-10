from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
import logging

# input parser
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('text')
parser.add_argument('tags', action='append')

class ElementsListApi(Resource):
  @marshal_with(element_fields)
  def get(self):
    elements = db.session.query(Element).all()
    return elements

  @marshal_with(element_fields)
  def post(self):
    args = parser.parse_args()
    logging.info('input: {json}'.format(json= args))
    try:

      # TODO : améliorer ce code inadmissible :D
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