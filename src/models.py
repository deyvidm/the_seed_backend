#!flas/bin/python
from src import db
from sqlalchemy.sql import func

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

