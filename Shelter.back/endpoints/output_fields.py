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
  # 'creation_date': fields.DateTime,
  # 'update_date': fields.DateTime,
  'tags': fields.List(fields.Nested(tag_fields), attribute='tags_associated')
}