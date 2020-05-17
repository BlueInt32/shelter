import io
import binascii
from PIL import Image
import urllib.request
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


class ElementsListApi(Resource):
    @marshal_with(element_fields)
    def get(self):
        elements = db.session.query(Element).all()
        return elements
