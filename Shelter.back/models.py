from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey(
                    'tag.id'), primary_key=True),
                db.Column('element_id', db.Integer, db.ForeignKey(
                    'element.id'), primary_key=True),
                )


class Element(db.Model):
  def __init__(self, title, text, input_tags):
    self.title = title
    self.text = text
    self.creation_date = datetime.utcnow()
    self.update_date = datetime.utcnow()
    self.tags_associated = input_tags

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), unique=False, nullable=False)
  text = db.Column(db.String(200), unique=False, nullable=True)
  creation_date = db.Column(db.DateTime, nullable=False)
  update_date = db.Column(db.DateTime, nullable=False)
  tags_associated = db.relationship('Tag', secondary=tags, lazy='subquery',
                                    backref=db.backref('elements_associated', lazy=True))
  attached_file = db.Column(db.LargeBinary, nullable=True)
  attached_thumb = db.Column(db.LargeBinary, nullable=True)

  # def __repr__(self):
  #     return '<Element %r>' % self.title


class Tag(db.Model):
  def __init__(self, label):
    self.label = label

  id = db.Column(db.Integer, primary_key=True)
  label = db.Column(db.String(200), unique=True, nullable=False)
