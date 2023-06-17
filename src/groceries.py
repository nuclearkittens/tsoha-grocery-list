'''Module for performing grocery list actions.'''

from datetime import datetime
from sqlalchemy.sql import text

from db import db

def _get_unique_items(items):
    '''Remove duplicate entries from a grocery list.'''
    unique_items = {}
    for item in items:
        key = (item['name'], item['uom'], item['category'])
        if key in unique_items:
            unique_items[key]['quantity'] += item['quantity']
        else:
            unique_items[key] = item

    return list(unique_items.values)

def get_list(list_id):
    query = text(
        '''SELECT c.name AS category, i.name AS item, g.quantity
        FROM grocery_list_items g
        JOIN items i ON i.id=g.item_id
        JOIN categories c ON c.id=i.cat_id
        WHERE g.list_id=:list_id
        ORDER BY c.name, i.name
        '''
    )
    res = db.session.execute(query, {'list_id': list_id}).fetchall()

    groceries = {}
    for cat, item, uom, qty in res:
        if cat not in groceries:
            groceries[cat] = {}
        groceries[cat][item] = (qty, uom)

    return groceries

def get_categories():
    '''Return a list of categories.'''
    query = text('SELECT name FROM categories')
    return db.session.execute(query).fetchall()

def _new_list(user_id, date, name):
    '''Create a new entry in the database and
    return the identifier of the new list.
    '''
    query = text(
        '''INSERT INTO grocery_list (user_id, date, name)
        VALUES (:user_id, :date, :name)
        '''
    )
    db.session.execute(
        query,
        {'user_id': user_id, 'date': date, 'name': name}
    )
    db.commit()

    query = text(
        '''SELECT id FROM grocery_list
        WHERE user_id=:user_id
        ORDER BY created_at DESC
        LIMIT 1
        '''
    )

    return db.session.execute(query, {'user_id': user_id}).fetchone()


def save_list(user_id, items, list_name=None, list_id=None):
    if not list_id:
        created_at = datetime.today().strftime('%Y-%m-%d')
        if not list_name:
            list_name = f'grocery list {created_at}'
        list_id = _new_list(user_id, created_at, list_name)
    else:
        pass


    items = _get_unique_items(items)