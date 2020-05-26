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
from services.media_service import save_element_with_video_link
from domain.enums import PersistanceType
import urllib.request
from PIL import Image
import binascii
import io
# input parser


class VideoLinksApi(Resource):
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

        new_element = save_element_with_video_link(PersistanceType.CREATE, args)

        return new_element, 201

    @marshal_with(element_fields)
    def put(self, element_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, help='Title of the image to download')
        parser.add_argument('text', type=str, help='Detail text of the image to download')
        parser.add_argument('linkUrl', type=str, help='Url of the image to download')
        parser.add_argument('tags', action='append')

        args = parser.parse_args()
        args['id'] = element_id

        element = save_element_with_video_link(PersistanceType.UPDATE, args)

        return element, 201
