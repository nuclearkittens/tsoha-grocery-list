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

def get_category_id(category):
    '''Return category identifier if category exists.'''
    query = text('SELECT id FROM categories c WHERE c.name=:category')
    res = db.session.execute(query).fetchone()

    return res[0] if res else None

def get_item_id(item):
    '''Get identifier for an item. If the item does not exist,
    an entry for it is created in the database.
    '''
    query_get = text(
        '''
        SELECT id FROM items i
        JOIN categories c ON c.id=i.cat_id
        WHERE is.name=:name
            AND i.uom=:uom AND c.name=:category
        '''
    )
    query_add = text('INSERT INTO items (name, uom, cat_id) VALUES (:name, :uom, :cat_id)')

    res = db.session.execute(query_get, item).fetchone()

    item_id = res[0] if res else None
    if not item_id:
        db.session.execute(query_add, {
            'name': item['name'],
            'uom': item['uom'],
            'cat_id': get_category_id(item['category'])
        })
        db.session.commit()
        res = db.session.execute(query_get, item).fetchone()
        item_id = res[0] if res else None

    return item_id

def get_list_items(list_id):
    query = text(
        '''
        SELECT i.name, l.quantity, i.uom, c.name AS category
        FROM items AS i
        JOIN grocery_list_items AS l ON l.item_id=i.id
        JOIN grocery_list AS g ON g.id=l.list_id
        JOIN categories AS c ON c.id=i.cat_id
        WHERE g.id=:list_id
        '''
    )
    res = db.session.execute(query, {'list_id': list_id}).fetchall()

    items = []
    for row in res:
        item = {
            'name': row.name,
            'quantity': row.quantity,
            'uom': row.uom,
            'category': row.category
        }
        items.append(item)

    return items

def get_sorted_list(list_id):
    '''Fetch an existing list from database, sorted based on category.

    param:
        list_id: int: list identifier
    return:
        dict: category name as key, value is a nested dictionary
        with the item name as key and
        quantity + unit of measurement as value
    '''
    query = text(
        '''
        SELECT c.name AS cat, i.name AS item, g.quantity AS qty
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

def new_list(user_id, list_name=None):
    '''Create a new entry in the database and
    return the identifier of the new list.
    '''
    created_at = datetime.today().strftime('%Y-%m-%d')
    if not list_name:
        list_name = f'grocery list {created_at}'

    query = text(
        '''
        INSERT INTO grocery_list (user_id, created_at, name)
        VALUES (:user_id, :created_at, :name)
        '''
    )
    db.session.execute(
        query,
        {'user_id': user_id, 'created_at': created_at, 'name': list_name}
    )
    db.commit()

    query = text(
        '''
        SELECT id FROM grocery_list
        WHERE user_id=:user_id
        ORDER BY created_at DESC
        LIMIT 1
        '''
    )
    list_id = db.session.execute(query, {'user_id': user_id}).fetchone()

    return list_id[0] if list_id else None

def _add_item(item_id, item):


def _update_quantity(list_id):
    pass

def save_list(list_id, items):
    items = _get_unique_items(items)

    for item in items:
