from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
import logging
import werkzeug
import sys
import psycopg2
from werkzeug.datastructures import ImmutableMultiDict
import json
from services.tags_service import resolve_tags
import urllib.request
from PIL import Image
import binascii
import io
# input parser


class ElementsListApi(Resource):
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

    if payloadFile is not None:
      parsed = json.loads(payloadFile.read().decode("utf-8"))
      print(parsed['title'])

    tags_associated = resolve_tags(parsed['tags'])
    new_element = Element(parsed['title'], parsed['text'], tags_associated)
    if 'file' in data:
      imageFile = data['file'][0]
      new_element.attached_file = imageFile.stream.read()
    if parsed['linkUrl'] is not '':
      # download media
      response = urllib.request.urlopen(parsed['linkUrl'])
      data = response.read()
      new_element.attached_file = data

    # thumbnail generation

    if new_element.attached_file is not None:
      stream = io.BytesIO(new_element.attached_file)
      im = Image.open(stream)
      im.thumbnail((128, 128))
      # im.save(outfile, "JPEG")
      imgByteArr = io.BytesIO()
      im.convert('RGB').save(imgByteArr, "JPEG")
      new_element.attached_thumb = imgByteArr.getvalue()

    db.session.add(new_element)
    db.session.commit()
    return new_element, 201


# # creating a object
# image = Image.open(r"C:\Users\System-Pc\Desktop\python.png")
# MAX_SIZE = (100, 100)

# image.thumbnail(MAX_SIZE)

# db.session.add(new_element)
# db.session.commit()
