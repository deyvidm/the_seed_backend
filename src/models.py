from src import db
from sqlalchemy.sql import func

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)

class Location(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)

class Entries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("Location.id"))
    # Decimal(10,2) is a number with 8 digits before the decimal and 2 digts after
    price = db.column(db.Float(10,2))
    name = db.Column(db.String(100), index=True, unique=True)
    date = db.Column(db.DateTime, default=func.now())

