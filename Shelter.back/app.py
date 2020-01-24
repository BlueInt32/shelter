from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

from database_setup import Base, Book

# Connect to Database and create database session
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username


# landing page that will display all the books in our database
# This function operate on the Read operation.
@app.route('/')
@app.route('/books')
def show_books():
    books = db.session.query(Book).all()
    return render_template("books.html", books=books)


# This will let us Create a new book and save it in our database
@app.route('/books/new/', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        new_book = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('show_books'))
    else:
        return render_template('new_book.html')


# This will let us Update our books and save it in our database
@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def edit_book(book_id):
    edited_book = db.session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edited_book.title = request.form['name']
            edited_book.author = request.form['author']
            edited_book.genre = request.form['genre']
            db.session.commit()
            return redirect(url_for('show_books'))
    else:
        return render_template('edit_book.html', book=edited_book)


# This will let us Delete our book
@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def delete_book(book_id):
    book_to_delete = db.session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect(url_for('show_books', book_id=book_id))
    else:
        return render_template('delete_book.html', book=book_to_delete)


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=4996)