from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Book

# Connect to Database and create database session
engine = create_engine('sqlite:///books-collection.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# landing page that will display all the books in our database
# This function operate on the Read operation.
@app.route('/')
@app.route('/books')
def show_books():
    books = DBSession().query(Book).all()
    return render_template("books.html", books=books)


# This will let us Create a new book and save it in our database
@app.route('/books/new/', methods=['GET', 'POST'])
def new_book():
    if request.method == 'POST':
        newBook = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        DBSession().add(newBook)
        DBSession().commit()
        return redirect(url_for('show_books'))
    else:
        return render_template('newBook.html')


# This will let us Update our books and save it in our database
@app.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def edit_book(book_id):
    editedBook = DBSession().query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.title = request.form['name']
            return redirect(url_for('show_books'))
    else:
        return render_template('editBook.html', book=editedBook)


# This will let us Delete our book
@app.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def delete_book(book_id):
    bookToDelete = DBSession().query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        DBSession().delete(bookToDelete)
        DBSession().commit()
        return redirect(url_for('show_books', book_id=book_id))
    else:
        return render_template('deleteBook.html', book=bookToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run()
    # app.run(host='0.0.0.0', port=4996)
