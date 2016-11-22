#!flas/bin/python
from src import db
from sqlalchemy.sql import func

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    entries = db.relationship('Entry', backref='food', lazy='dynamic')

class Location(db.Model): 
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)

class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    # Decimal(10,2) is a number with 8 digits before the decimal and 2 digts after
    price = db.column(db.Float(10,2))
    name = db.Column(db.String(100), index=True, unique=True)
    date = db.Column(db.DateTime)

