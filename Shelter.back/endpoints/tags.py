from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import tag_fields
from models import db, Element, Tag

class TagsSearchApi(Resource):
  @marshal_with(tag_fields)
  def get(self, search_term):
    results = Tag.query.filter(Tag.label.like(search_term + '%')).all()
    return results