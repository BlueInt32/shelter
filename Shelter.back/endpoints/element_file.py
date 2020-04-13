import io
from flask import send_file
from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
from services.tags_service import resolve_tags


def build_http_response_from_file(db_element_title, db_blob):
  response = send_file(
      io.BytesIO(db_blob),
      as_attachment=True,
      attachment_filename=db_element_title+'.jpg',
      # attachment_filename='logo.jpeg',
      mimetype='image/jpg'
  )
  # this header makes browser display image directly instead of
  # suggesting download popup
  response.headers['Content-disposition'] = 'inline'
  return response


class ElementFileApi(Resource):
  def get(self, element_id):
    retrieved_element = Element.query.get_or_404(element_id)
    return build_http_response_from_file(retrieved_element.title, retrieved_element.attached_file)


class ElementThumbnailFileApi(Resource):
  def get(self, element_id):
    retrieved_element = Element.query.get_or_404(element_id)
    retrieved_element = Element.query.get_or_404(element_id)
    return build_http_response_from_file(retrieved_element.title, retrieved_element.attached_thumb)
