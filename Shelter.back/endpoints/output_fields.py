from flask_restful import reqparse, Resource, Api, fields, marshal_with

# output fields
tag_fields = {
    'id': fields.Integer,
    'label': fields.String
}
element_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    'linkUrl': fields.String(attribute='link_url'),
    'creationDate': fields.DateTime(dt_format='iso8601', attribute='creation_date'),
    'updateDate': fields.DateTime(dt_format='iso8601', attribute='update_date'),
    'tags': fields.List(fields.Nested(tag_fields), attribute='tags_associated'),
    'type': fields.String
}
