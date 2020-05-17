from flask_restful import reqparse, Resource, Api, fields, marshal_with
from endpoints.output_fields import element_fields
from models import db, Element, Tag
from services.tags_service import resolve_tags
import json
from dateutil import tz


class ElementDetailApi(Resource):
    @marshal_with(element_fields)
    def get(self, element_id):
        retrieved_element = Element.query.get_or_404(element_id)
        to_zone = tz.tzlocal()
        from_zone = tz.tzutc()
        retrieved_element.creation_date = retrieved_element.creation_date.replace(
            tzinfo=from_zone).astimezone(to_zone)

        return retrieved_element

    @marshal_with(element_fields)
    def put(self, element_id):
        # 1 retrieve both parts of the multipart
        parts = dict(reqparse.request.files)
        jsonFile = parts['payload'][0]

        parsedJson = json.loads(jsonFile.read().decode("utf-8"))
        print(parsedJson['title'])

        db_element = Element.query.get_or_404(element_id)
        db_element.title = parsedJson['title']
        db_element.text = parsedJson['text']
        db_element.tags_associated = resolve_tags(parsedJson['tags'])

        if 'file' in parts:
            file = parts['file'][0]
            db_element.attached_file = file.stream.read()

        db.session.commit()
        return db_element, 200

    def delete(self, element_id):
        retrieved_element = Element.query.get(element_id)
        db.session.delete(retrieved_element)
        db.session.commit()
        return 204
