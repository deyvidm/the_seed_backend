#!flask/bin/python
from src import db, models 
from datetime import datetime

now = datetime.now()

p = []
l = []
e = []

p.append(models.Product(name="Carrots"))
p.append(models.Product(name="Baby Carrots"))
p.append(models.Product(name="Baby-cut Carrots"))

l.append(models.Location(name="Metro"))
l.append(models.Location(name="Zehrs"))
l.append(models.Location(name="Loballs"))

e.append(models.Entry(product_id=1, location_id=1, price=1.11, date=now))
e.append(models.Entry(product_id=2, location_id=1, price=1.11, date=now))

e.append(models.Entry(product_id=1, location_id=2, price=2.22, date=now))
e.append(models.Entry(product_id=1, location_id=2, price=2.22, date=now))

e.append(models.Entry(product_id=3, location_id=3, price=3.33, date=now))
e.append(models.Entry(product_id=3, location_id=3, price=3.33, date=now))

for i in p+l+e:
    print i
    db.session.add(i)
    
db.session.commit()
