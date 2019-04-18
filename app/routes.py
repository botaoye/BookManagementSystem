from app import app
from app.models import Book, Inventory
from flask import render_template, request, jsonify

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/search_book', methods=['GET', 'POST'])
def search_book():
    if request.method == 'GET':
        return render_template('search_book.html')
    else:
        def find_name():
            return Book.query.filter(Book.book_name.like('%'+request.form.get('content')+'%')).all()

        def find_author():
            return Book.query.filter(Book.author.contains(request.form.get('content'))).all()

        def find_class():
            return Book.query.filter(Book.class_name.contains(request.form.get('content'))).all()

        def find_isbn():
            return Book.query.filter(Book.isbn.contains(request.form.get('content'))).all()

        methods = {
            'book_name': find_name,
            'author': find_author,
            'class_name': find_class,
            'isbn': find_isbn
        }
        books = methods[request.form.get('method')]()
        data = []
        for book in books:
            count = Inventory.query.filter_by(isbn=book.isbn).count()
            available = Inventory.query.filter_by(isbn=book.isbn, status=True).count()
            item = {'isbn': book.isbn, 'book_name': book.book_name, 'press': book.press, 'author': book.author,
                    'class_name': book.class_name, 'count': count, 'available': available}
            data.append(item)
        return jsonify({"data": data})

