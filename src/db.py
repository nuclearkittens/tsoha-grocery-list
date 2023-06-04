'''Module for initialising the database connection.'''

from os import getenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    '''Initialise the database.'''
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL") # or postgresql+psycopg2://
    db.init_app(app)
