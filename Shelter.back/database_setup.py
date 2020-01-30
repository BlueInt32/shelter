from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time

app = Flask(__name__)

POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "Simon"
POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
POSTGRES_DB = "shelter"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)

tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                db.Column('element_id', db.Integer, db.ForeignKey('element.id'), primary_key=True),
                )


class Element(db.Model):
    def __init__(self, title, text, input_tags):
        self.title = title
        self.text = text
        self.creation_date = datetime.utcnow()
        self.update_date = datetime.utcnow()
        self.tags = input_tags

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    text = db.Column(db.String(200), unique=False, nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)
    tags_associated = db.relationship('Tag', secondary=tags, lazy='subquery',
                                      backref=db.backref('elements_associated', lazy=True))

    # def __repr__(self):
    #     return '<Element %r>' % self.title


class Tag(db.Model):
    def __init__(self, label):
        self.label = label

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), unique=True, nullable=False)


@app.route('/element')
def create_element():
    user = Element(title="Coucou", text="this is a test", tags=[])

    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'name': user.name, 'job': user.job}


@app.route('/resetdb', methods=['get'])
def reset_db():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    status = ''
    if database_exists(DB_URL):
        print('Deleting database.')
        status += 'delete '
        # db.drop_all(bind=['element_tag', 'tag', 'element'])
        db.drop_all()
        drop_database(DB_URL)
    time.sleep(1)
    if not database_exists(DB_URL):
        print('Creating database.')
        status += 'create '
        create_database(DB_URL)
        db.create_all()

    # db.create_all()

    return 'OK ' + status


if __name__ == '__main__':
    app.debug = True
    app.run(port=5001)
