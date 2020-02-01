from flask_restful import reqparse, Resource, Api, fields, marshal_with
from models import db, Element, Tag
import logging
import sys



# output fields
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

# input parser
parser = reqparse.RequestParser()
parser.add_argument('title')
parser.add_argument('text')
parser.add_argument('tags', action='append')

#endpoints definitions
class ElementApi(Resource):
  @marshal_with(element_fields)
  def get(self, element_id):
    retrieved_element = Element.query.get_or_404(element_id)
    return retrieved_element

  def put(self, element_title):
    args = parser.parse_args(strict=True)
    new_element = Element(args['title'].title)
    db.session.add(new_element)
    db.session.commit()
    return new_element, 201

  def delete(self, element_id):
    retrieved_element = Element.query.get(element_id)
    db.session.delete(retrieved_element)
    db.session.commit()
    return 204


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


class TagsSearchApi(Resource):
  @marshal_with(tag_fields)
  def get(self, search_term):
    results = Tag.query.filter(Tag.label.like(search_term + '%')).all()
    return results
