import io
import binascii
from PIL import Image
import urllib.request
from flask_restful import reqparse, Resource, Api, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
import logging
import werkzeug
import sys
import psycopg2
from werkzeug.datastructures import ImmutableMultiDict
import json
from services.tags_service import resolve_tags
from flask import jsonify

class ElementsListApi(Resource):
    def get(self):
        elements = db.session.query(Element.id, Element.title, Element.type, Element.link_url).all()
        output = [{'id': el.id, 'title': el.title, 'type': el.type, 'linkUrl': el.link_url} for el in elements]
        return output
