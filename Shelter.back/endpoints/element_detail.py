from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('text')
parser.add_argument('tags', action='append')

class ElementApi(Resource):
  @marshal_with(element_fields)
  def get(self, element_id):
    retrieved_element = Element.query.get_or_404(element_id)
    return retrieved_element

  @marshal_with(element_fields)
  def put(self, element_id):
    retrieved_element = Element.query.get_or_404(element_id)
    args = parser.parse_args(strict=True)
    retrieved_element.title = args['title']
    retrieved_element.text = args['text']

    # TODO : améliorer ce code inadmissible :D
    already_existing_tags = Tag.query.filter(Tag.label.in_(args.tags or [])).all()
    already_existing_tags_labels = set(map(lambda t: t.label, already_existing_tags))
    received_tags = set(args.tags or [])
    new_tags = [Tag(t) for t in (received_tags - already_existing_tags_labels)]
    all_tags_to_add = set(new_tags) | set(already_existing_tags)
    retrieved_element.tags_associated = list(all_tags_to_add)

    # TODO : handle tags here
    db.session.commit()
    return retrieved_element, 201

  def delete(self, element_id):
    retrieved_element = Element.query.get(element_id)
    db.session.delete(retrieved_element)
    db.session.commit()
    return 204