import datetime
from app import db, login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(6), primary_key=True)
    user_name = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(24))
    privilidge = db.Column(db.String(1))  # 用户权限（0 for super_admin, 1 for admin, 2 for reader）

    def __init__(self, user_id, user_name, password, privilidge):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.privilidge = privilidge

    def get_id(self):
        return self.user_id

    def verify_password(self, password):
        if password == self.password:
            return True
        else:
            return False

    def __repr__(self):
        return '<User %r>' % self.user_name


class AdminUser(db.Model):
    __tablename__ = 'adminuser'
    admin_id = db.Column(db.ForeignKey('user.user_id'), primary_key=True)
    admin_name = db.Column(db.String(32))
    privilidge = db.Column(db.String(1))  # 用户权限（0 for super_admin, 1 for admin）

    def __repr__(self):
        return '<AdminUser %r>' % self.admin_name


# 图书管理数据表
class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(13), primary_key=True)
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    press = db.Column(db.String(64))
    class_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Book %r>' % self.book_name


class LibraryCard(db.Model):
    __tablename__ = 'librarycard'
    card_id = db.Column(db.ForeignKey('user.user_id'), primary_key=True)
    name = db.Column(db.String(32))
    sex = db.Column(db.String(8))
    telephone = db.Column(db.String(11), nullable=True)
    enroll_date = db.Column(db.Date)
    valid_date = db.Column(db.Date)
    loss = db.Column(db.Boolean, default=False)  # 是否挂失
    debt = db.Column(db.Boolean, default=False)  # 是否欠费

    def __repr__(self):
        return '<LibraryCard %r>' % self.name


class Inventory(db.Model):
    __tablename__ = 'inventory'
    barcode = db.Column(db.String(6), primary_key=True)
    isbn = db.Column(db.ForeignKey('book.isbn'))
    storage_date = db.Column(db.Date)
    location = db.Column(db.String(32))
    status = db.Column(db.Boolean, default=True)  # 是否在馆
    admin = db.Column(db.ForeignKey('adminuser.admin_id'))  # 入库操作员

    def __repr__(self):
        return '<Inventory %r>' % self.barcode


class ReadBook(db.Model):
    __tablename__ = 'readbook'
    operation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.ForeignKey('inventory.barcode'), index=True)
    borrow_user = db.Column(db.ForeignKey('user.user_id'))  # 借书者
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date)  # 应还日期

    def change_end_date(self):
        self.end_date = str(datetime.date.today())

    def __repr__(self):
        return '<ReadBook %r>' % self.operation_id


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)