#!flask/bin/python
from src import app, db, models
from flask import jsonify
import simplejson as json
from datetime import datetime
import sys

def scraperToDB(scraper_JSON):
    obj = json.loads(scraper_JSON)
    #find products in JSON
    for loc, products in obj.iteritems():
        loc = loc.lower()
        for prod, cost in products.iteritems():
            print prod, cost
            prod = prod.lower()
            #try to get a product ID 
            #if the product is not in the database, add it and then get its id
            while True: 
                p = models.Product.query.filter_by(name=prod).first()
                if p: 
                    break;
                db.session.add(models.Product(name=prod))
                db.session.commit()
             
            while True: 
                l = models.Location.query.filter_by(name=loc).first()
                if l: 
                    break;
                db.session.add(models.Location(name=loc))
                db.session.commit()           
            
            e = (models.Entry(product_id=p.id, location_id=l.id, 
                            price=cost, date=datetime.now()))
            db.session.add(e)
    db.session.commit()

for arg in sys.argv[1:]:
    with open(arg, 'r') as in_file: 
        scraperToDB(in_file.read())
