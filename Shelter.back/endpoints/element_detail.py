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

    def delete(self, element_id):
        retrieved_element = Element.query.get(element_id)
        db.session.delete(retrieved_element)
        db.session.commit()
        return 204
