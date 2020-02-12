from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
import logging
import werkzeug
import sys
from werkzeug.datastructures import ImmutableMultiDict
import json
from services.tags_service import resolve_tags

# input parser


class ElementsListApi(Resource):
  def parse_utf8(self, bytes, length_size):
    length = bytes2int(bytes[0:length_size])
    value = ''.join(['%c' % b for b in bytes[length_size:length_size+length]])
    return value

  @marshal_with(element_fields)
  def get(self):
    elements = db.session.query(Element).all()
    return elements

  @marshal_with(element_fields)
  def post(self):
    parser = reqparse.RequestParser()
    # parser.add_argument('id',)
    # parser.add_argument('title', location='files')
    # parser.add_argument('text', location='files')
    # parser.add_argument('tags', action='append', location= 'files')
    # parser.add_argument('payload', type=werkzeug.FileStorage, location='files')
    # parser.add_argument('file', type=werkzeug.FileStorage, location='files')

    data = dict(reqparse.request.files)
    payloadFile = data['payload'][0]
    if 'file' in data:
      imageFile = data['file'][0]

    if payloadFile is not None:
      parsed = json.loads(payloadFile.read().decode("utf-8"))
      print(parsed['title'])

    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(parsed['title'], parsed['text'], tags_associated)
    new_element.attached_file = imageFile

    db.session.add(new_element)
    db.session.commit()
    return new_element, 201

