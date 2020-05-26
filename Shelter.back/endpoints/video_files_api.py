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
from services.media_service import save_element_with_video_file
from domain.enums import PersistanceType
import urllib.request
from PIL import Image
import binascii
import io
# input parser


class VideoFilesApi(Resource):
    @marshal_with(element_fields)
    def get(self):
        elements = db.session.query(Element).all()
        return elements

    @marshal_with(element_fields)
    def post(self):
        parser = reqparse.RequestParser()

        data = dict(reqparse.request.files)

        new_element = save_element_with_video_file(PersistanceType.CREATE, data)

        return new_element, 201

    @marshal_with(element_fields)
    def put(self, element_id):
        parser = reqparse.RequestParser()

        data = dict(reqparse.request.files)

        new_element = save_element_with_video_file(PersistanceType.UPDATE, data)

        return new_element, 201
