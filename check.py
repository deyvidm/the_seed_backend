#!flask/bin/python
from sqlalchemy import create_engine
from sqlalchemy import inspect

engine = create_engine("sqlite:///app.db")
inspector = inspect(engine)

for table_name in inspector.get_table_names():
    print table_name
    for column in inspector.get_columns(table_name):
        print("Column: %s" % column['name'])
    print "========================="
