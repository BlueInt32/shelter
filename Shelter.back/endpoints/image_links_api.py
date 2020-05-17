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
from services.media_service import handle_image_link
import urllib.request
from PIL import Image
import binascii
import io
# input parser


class ImageLinksApi(Resource):
    @marshal_with(element_fields)
    def get(self):
        elements = db.session.query(Element).all()
        return elements

    @marshal_with(element_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Title of the image to download')
        parser.add_argument('text', type=str, help='Detail text of the image to download')
        parser.add_argument('linkUrl', type=str, help='Url of the image to download')
        parser.add_argument('tags', action='append')

        args = parser.parse_args()

        # data = dict(reqparse.request.files)

        new_element = handle_image_link(args)

        return new_element, 201


# # creating a object
# image = Image.open(r"C:\Users\System-Pc\Desktop\python.png")
# MAX_SIZE = (100, 100)

# image.thumbnail(MAX_SIZE)

# db.session.add(new_element)
# db.session.commit()
