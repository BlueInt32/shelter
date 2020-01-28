from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES_URL = "127.0.0.1:5432"
POSTGRES_USER = "Simon"
POSTGRES_PW = "t2vlYfAMm5VXhvlyhY12fj"
POSTGRES_DB = "shelter"

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                               db=POSTGRES_DB)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shelter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning

db = SQLAlchemy(app)


class Element(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=False, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)


@app.route('/element')
def create_element():
    user = Element(title="Coucou", description="this is a test")
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
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        status += 'create '
        create_database(DB_URL)

    db.create_all()
    return 'OK ' + status
