from app import db
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(6), primary_key=True)
    user_name = db.Column(db.String(32))
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


class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.ForeignKey('user.user_id'), primary_key=True)
    admin_name = db.Column(db.String(32))
    privilidge = db.Column(db.String(1))  # 用户权限（0 for super_admin, 1 for admin）


# 图书管理数据表
class Book(db.Model):
    __tablename__ = 'book'
    isbn = db.Column(db.String(13), primary_key=True)
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    press = db.Column(db.String(32))
    class_name = db.Column(db.String(64))

    def __repr__(self):
        return '<Book %r>' % self.book_name


class LibraryCard(db.Model):
    __tablename__ = 'librarycard'
    card_id = db.Column(db.ForeignKey('user.user_id'), primary_key=True)
    name = db.Column(db.String(32))
    sex = db.Column(db.String(2))
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
    admin = db.Column(db.ForeignKey('admin.admin_id'))  # 入库操作员

    def __repr__(self):
        return '<Inventory %r>' % self.barcode


class ReadBook(db.Model):
    __tablename__ = 'readbook'
    operation_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.ForeignKey('inventory.barcode'), index=True)
    card_id = db.Column(db.ForeignKey('librarycard.card_id'), index=True)
    borrow_user = db.Column(db.ForeignKey('user.user_id'))  # 借书者
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date)  # 应还日期

    def __repr__(self):
        return '<ReadBook %r>' % self.operation_id