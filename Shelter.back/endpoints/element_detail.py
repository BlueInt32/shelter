from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
from services.tags_service import resolve_tags


class ElementApi(Resource):
  @marshal_with(element_fields)
  def get(self, element_id):
    retrieved_element = Element.query.get_or_404(element_id)
    return retrieved_element

  @marshal_with(element_fields)
  def put(self, element_id):
    parser = reqparse.RequestParser()
    parser.add_argument('id')
    parser.add_argument('title')
    parser.add_argument('text')
    parser.add_argument('tags', action='append')

    retrieved_element = Element.query.get_or_404(element_id)
    args = parser.parse_args(strict=True)
    retrieved_element.title = args['title']
    retrieved_element.text = args['text']
    retrieved_element.tags_associated = resolve_tags(args.tags)

    db.session.commit()
    return retrieved_element, 201

  def delete(self, element_id):
    retrieved_element = Element.query.get(element_id)
    db.session.delete(retrieved_element)
    db.session.commit()
    return 204