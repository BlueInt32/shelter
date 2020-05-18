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
    'link_url': fields.String,
    'creation_date': fields.DateTime(dt_format='iso8601'),
    'update_date': fields.DateTime(dt_format='iso8601'),
    'tags': fields.List(fields.Nested(tag_fields), attribute='tags_associated'),
    'type': fields.String
}
