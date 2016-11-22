import os 
basedir = os.path.abspath(os.path.dirname(__file__))

#required by SQLAlchemy 
#where we store the databse file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

#where we store migration files 
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

#to suppress warning
SQLALCHEMY_TRACK_MODIFICATIONS = True
