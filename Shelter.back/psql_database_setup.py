from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# the values of those depend on your setup
POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "Simon"
POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
POSTGRES_DB = "test"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    author = db.Column(db.String(200), unique=False, nullable=True)
    genre = db.Column(db.String(200), unique=False, nullable=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=True)
    job = db.Column(db.String(200), unique=False, nullable=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.spotify_id


@app.route('/user')
def lolz():
    user = User(name="Simon", job="developer")
    db.session.add(user)
    db.session.commit()
    return {'id': user.id, 'name': user.name, 'job': user.job}


@app.route('/resetdb', methods=['post'])
def resetdb():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Shiny!')
    return 'OK'
