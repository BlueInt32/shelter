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
    def __init__(self, title, text, input_tags, element_type, link):
        self.title = title
        self.text = text
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
        self.tags_associated = input_tags
        self.type = element_type
        self.link_url = link

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    link_url = db.Column(db.String(500), unique=False, nullable=True)
    text = db.Column(db.String(200), unique=False, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)
    tags_associated = db.relationship('Tag', secondary=tags, lazy='subquery',
                                      backref=db.backref('elements_associated', lazy=True))
    attached_file = db.Column(db.LargeBinary, nullable=True)
    attached_thumb = db.Column(db.LargeBinary, nullable=True)
    type = db.Column(db.String(10), unique=False, nullable=False)

    # def __repr__(self):
    #     return '<Element %r>' % self.title


class Tag(db.Model):
    def __init__(self, label):
        self.label = label

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), unique=True, nullable=False)
