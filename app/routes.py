import datetime
from app import app, db
from app.models import Book, Inventory, LibraryCard, User, AdminUser, ReadBook
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search_book'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('search_book'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/index')
@app.route('/search_book', methods=['GET', 'POST'])
@login_required
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
        books = methods[request.form.get('search_book_method_selector')]()
        data = []
        for book in books:
            count = Inventory.query.filter_by(isbn=book.isbn).count()
            available = Inventory.query.filter_by(isbn=book.isbn, status=True).count()
            item = {'isbn': book.isbn, 'book_name': book.book_name, 'press': book.press, 'author': book.author,
                    'class_name': book.class_name, 'count': count, 'available': available}
            data.append(item)
        return jsonify(data)


@app.route('/manage_library_card', methods=['GET', 'POST'])
@login_required
def manage_library_card():
    if request.method == 'GET':
        return render_template('manage_library_card.html')
    else:
        post_method = request.form.get('post_method')
        user = User(request.form.get('card_id'), request.form.get('card_id'), request.form.get('card_id'), '2')
        record = LibraryCard(card_id=request.form.get('card_id'), name=request.form.get('name'), sex=request.form.get('sex'), telephone=request.form.get('telephone'), 
                enroll_date=request.form.get('enroll_date'), valid_date=request.form.get('valid_date'), loss=int(request.form.get('loss')), debt=int(request.form.get('debt')))
        if post_method == 'add':
            if User.query.filter_by(user_id=request.form.get('card_id')).first() is None:
                db.session.add(user)
                db.session.commit()
                print("user added")
            db.session.add(record)
            print("card added")
            db.session.commit()
        elif post_method == 'change':
            delete_item = LibraryCard.query.filter_by(card_id=request.form.get('card_id')).first()
            db.session.delete(delete_item)
            db.session.add(record)
            db.session.commit()
    
    return jsonify("success")
            


@app.route('/get_all_library_card', methods=['GET'])
def get_all_library_card():
    cards = LibraryCard.query.all()
    data = []
    for card in cards:
        item = {'card_id': card.card_id, 'name': card.name, 'sex': card.sex, 'telephone': card.telephone, 
                'enroll_date': card.enroll_date, 'valid_date': card.valid_date, 'loss': card.loss, 'debt':card.debt}
        data.append(item)
    return jsonify(data)

@app.route('/delete_library_card', methods=['POST'])
def delete_library_card():
    card_id = request.form.get('card_id')
    record = LibraryCard.query.filter_by(card_id=card_id).first()
    user = User.query.filter_by(user_id=card_id).first()
    db.session.delete(record)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    print("success")
    return jsonify("success")


@app.route('/manage_book', methods=['GET', 'POST'])
@login_required
def manage_book():
    if request.method == 'GET':
        return render_template('manage_book.html')
    else:
        inventory = Inventory(barcode=request.form.get('barcode'), isbn=request.form.get('isbn'), storage_date=request.form.get('storage_date'),
            location=request.form.get('location'), status=int(request.form.get('status')), admin=request.form.get('admin'))
        book = Book(isbn=request.form.get('isbn'), book_name=request.form.get('book_name'), author=request.form.get('author'),
                press=request.form.get('press'), class_name=request.form.get('class_name'))
        if Book.query.filter_by(isbn=request.form.get('isbn')).first() is None:
            db.session.add(book)
            db.session.commit()
        db.session.add(inventory)
        print("book added")
        db.session.commit()
    
    return jsonify("success")


@app.route('/get_all_book', methods=['GET'])
def get_all_book():
    inventories = Inventory.query.all()
    data = []
    for inventory in inventories:
        item = {'barcode': inventory.barcode, 'isbn': inventory.isbn, 'storage_date': inventory.storage_date,
            'location':inventory.location, 'status': inventory.status, 'admin': inventory.admin}
        data.append(item)
    return jsonify(data)

@app.route('/delete_book', methods=['POST'])
def delete_book():
    barcode = request.form.get('barcode')
    record = Inventory.query.filter_by(barcode=barcode).first()
    db.session.delete(record)
    db.session.commit()
    print("success")
    return jsonify("success")


@app.route('/manage_admin', methods=['GET', 'POST'])
@login_required
def manage_admin():
    if request.method == 'GET':
        return render_template('manage_admin.html')
    else:
        user = User(request.form.get('admin_id'), request.form.get('admin_id'), request.form.get('admin_id'), request.form.get('privilidge'))
        admin = AdminUser(admin_id=request.form.get('admin_id'), admin_name=request.form.get('admin_name'), privilidge=request.form.get('privilidge'))
        if User.query.filter_by(user_id=request.form.get('admin_id')).first() is None:
            db.session.add(user)
            db.session.commit()
            db.session.add(admin)
            db.session.commit()
            return jsonify("add admin success")
        
        return jsonify("id already existed")

@app.route('/get_all_admin', methods=['GET'])
def get_all_admin():
    admins = AdminUser.query.all()
    data = []
    for admin in admins:
        item = {'admin_id': admin.admin_id, 'admin_name': admin.admin_name, 'privilidge': admin.privilidge}
        data.append(item)
    return jsonify(data)

@app.route('/delete_admin', methods=['POST'])
def delete_admin():
    admin_id = request.form.get('admin_id')
    record = AdminUser.query.filter_by(admin_id=admin_id).first()
    user = User.query.filter_by(user_id=admin_id).first()
    db.session.delete(record)
    db.session.delete(user)
    db.session.commit()
    print("success")
    return jsonify("success")


@app.route('/return_book', methods=['GET', 'POST'])
@login_required
def return_book():
    if request.method == 'GET':
        return render_template('return_book.html')
    else:
        record = ReadBook.query.filter_by(operation_id=request.form.get('operation_id')).first()
        db.session.delete(record)
        record.change_end_date()
        db.session.add(record)

        inventory = Inventory.query.filter_by(barcode=request.form.get('barcode')).first()
        db.session.delete(inventory)
        inventory.status = True
        db.session.add(inventory)
        db.session.commit()
        return(jsonify("return book success"))

@app.route('/get_all_borrow_history', methods=['GET'])
def get_all_borrow_history():
    user_id = current_user.user_id
    print(user_id)
    records = ReadBook.query.filter_by(borrow_user=user_id).all()
    data = []
    for record in records:
        inventory = Inventory.query.filter_by(barcode=record.barcode).first()
        book = Book.query.filter_by(isbn=inventory.isbn).first()
        item = {'operation_id': record.operation_id, 'barcode': record.barcode, 'isbn': inventory.isbn, 'book_name': book.book_name,
                'start_date': record.start_date, 'due_date': record.due_date, 'end_date': record.end_date}
        data.append(item)
    return jsonify(data)

@app.route('/borrow_book', methods=['GET', 'POST'])
@login_required
def borrow_book():
    if request.method == 'GET':
        return render_template('borrow_book.html')
    else:
        inventory = Inventory.query.filter_by(barcode=request.form.get('barcode')).first()
        db.session.delete(inventory)
        inventory.status = False
        db.session.add(inventory)

        # 期限是4个月
        start_date = str(datetime.date.today()).split('-')
        start_date1 = str(datetime.date.today())
        if int(start_date[1]) >= 9:
            start_date[1] = str(int(start_date[1]) + 4 -12)
            start_date[0] = str(int(start_date[0]) + 1)
        else:
            start_date[1] = str(int(start_date[1]) + 4)
        due_date = start_date[0] + '-' + start_date[1] + '-' + start_date[2]

        readbook = ReadBook(barcode=request.form.get('barcode'), borrow_user=current_user.user_id, 
            start_date=start_date1, due_date=due_date)
        db.session.add(readbook)
        db.session.commit()
        return(jsonify("borrow book success"))

@app.route('/get_all_book_for_borrow', methods=['GET'])
def get_all_book_for_borrow():
    inventories = Inventory.query.all()
    data = []
    for inventory in inventories:
        book = Book.query.filter_by(isbn=inventory.isbn).first()
        item = {'barcode': inventory.barcode, 'isbn': inventory.isbn, 'book_name': book.book_name,
                'storage_date': inventory.storage_date, 'location':inventory.location, 'status': inventory.status}
        data.append(item)
    return jsonify(data)