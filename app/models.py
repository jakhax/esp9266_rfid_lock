import os,uuid
from . import db
from datetime import datetime
import pytz

from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import func
from . import login_manager


@login_manager.user_loader
def usergetter(uid):
	return Admin.query.get(uid)

class Admin(db.Model,UserMixin):
    __tablename__='admins'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(255),unique=True)
    email=db.Column(db.String(255),unique=True)
    password=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, index=True, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())

    def verifypass(self,pass_check):
        return check_password_hash(self.password,pass_check)

    @property
    def passwd(self):
        raise AttributeError('You cannot read this!')

    @passwd.setter
    def passwd(self,passwd):
        self.password = generate_password_hash(passwd)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Admin %r>' % self.username

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    uid=db.Column(db.String(255),unique=True)
    email=db.Column(db.String(255),unique=True)
    created_at = db.Column(db.DateTime, index=True, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())
    access=db.relationship('AccessLogs', backref='user', lazy='dynamic')

    def create_uid(self):
        # 2**16 - 1
        uid=bytearray(os.urandom(16)).hex()
        if User.query.filter_by(uid=uid).first():
            self.create_uid()
        self.uid=uid
        return uid

    def verifypin(self,pin):
        return check_password_hash(self.pin,pass_check)

    def set_pin(self,pin):
        self.pin = generate_password_hash(pin)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username


class AccessLogs(db.Model):
    __tablename__='access_logs'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, index=True, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())

    def save(self):
       
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.user_id

class FailedAccessLogs(db.Model):
    __tablename__='failed_access_logs'
    id=db.Column(db.Integer,primary_key=True)
    attempted_uid=db.Column(db.String(255))
    created_at = db.Column(db.DateTime, index=True, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<id %r>' % self.id