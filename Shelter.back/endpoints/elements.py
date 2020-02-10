from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
import logging
import werkzeug
import sys
from werkzeug.datastructures import ImmutableMultiDict
import json

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
    imageFile = data['file'][0]

    if payloadFile is not None:
      parsed = json.loads(payloadFile.read().decode("utf-8"))
      #print(parsed)
      print(parsed['title'])
    # args = parser.parse_args(strict=True)
      # payload = payloadFile.read().decode("utf-8")
      # payloadFile.save('coucou.json')
    # if imageFile is not None:
    #   imageFile.save('coucou.jpg')

    try:

      # TODO : améliorer ce code inadmissible :D
      already_existing_tags = Tag.query.filter(Tag.label.in_(parsed['tags'] or [])).all()
      already_existing_tags_labels = set(map(lambda t: t.label, already_existing_tags))
      received_tags = set(parsed['tags'] or [])
      new_tags = [Tag(t) for t in (received_tags - already_existing_tags_labels)]
      all_tags_to_add = set(new_tags) | set(already_existing_tags)
      new_element = Element(parsed['title'], parsed['text'], list(all_tags_to_add))

      db.session.add(new_element)
      db.session.commit()
      return new_element, 201
    except:
      print("Unexpected error:", sys.exc_info()[0])
      return 'Error', 400
