'''Module for performing grocery list actions.'''

from datetime import datetime
from sqlalchemy.sql import text

from db import db

def get_categories():
    '''Return a list of categories.'''
    query = text('SELECT name FROM categories')
    return db.session.execute(query).fetchall()

def save_list(items, list_name=None):
    created_at = datetime.today().strftime('%Y-%m-%d')

