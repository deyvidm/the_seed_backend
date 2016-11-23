#!flas/bin/python
from src import db, app
from sqlalchemy.sql import func
from flask import Flask
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer 
                          as Serializer, BadSignature, SignatureExpired)

# initialization
app.config['SECRET_KEY'] = 'i am legitimately so hungry right now'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    entries = db.relationship('Entry', backref='food', lazy='dynamic')

class Location(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    entries = db.relationship('Entry', backref='source', lazy='dynamic')

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    # Decimal(10,2) is a number with 8 digits before the decimal and 2 digts after
    price = db.Column(db.Float(10,2))
    date = db.Column(db.DateTime)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

