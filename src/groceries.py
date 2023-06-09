'''Module for performing grocery list actions.'''

from datetime import datetime, timezone
from secrets import token_urlsafe
from sqlalchemy.sql import text

from db import db

def get_category_dict():
    '''Return a dictionary of the category names and identifiers.'''
    query = text('SELECT name, id FROM categories')
    res = db.session.execute(query).fetchall()
    return {row.name: row.id for row in res}

def get_item_id(item):
    '''Get identifier for an item. If the item does not exist,
    an entry for it is created in the database.
    '''
    query_get = text(
        '''
        SELECT i.id FROM items i
        JOIN categories c ON c.id=i.cat_id
        WHERE i.name=:name AND i.uom=:uom AND c.id=:category
        '''
    )
    query_add = text('INSERT INTO items (name, uom, cat_id) VALUES (:name, :uom, :cat_id)')

    res = db.session.execute(query_get, item).fetchone()

    item_id = res[0] if res else None
    if not item_id:
        db.session.execute(query_add, {
            'name': item['name'],
            'uom': item['uom'],
            'cat_id': item['category']
        })
        db.session.commit()

        res = db.session.execute(query_get, item).fetchone()
        item_id = res[0] if res else None

    return item_id

def get_list_info(list_id):
    '''Return the name of the list.'''
    query = text('SELECT name, created_at, share_id FROM grocery_list WHERE id=:list_id')
    list_info = db.session.execute(query, {'list_id': list_id}).fetchone()
    return list_info if list_info else (None, None, None)

def get_list_items(list_id):
    '''Return a list of items and their information from
    a specified list.'''
    query = text(
        '''
        SELECT i.id, i.name, l.quantity, i.uom, c.name AS category
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
            'id': row.id,
            'name': row.name,
            'quantity': row.quantity,
            'uom': row.uom,
            'category': row.category
        }
        items.append(item)

    return items

def get_lists_by_user(user_id):
    '''Return the name and identifier of all
    grocery lists owned by an user.
    '''
    query = text(
        '''
        SELECT id, name FROM grocery_list
        WHERE user_id=:user_id
        ORDER BY created_at DESC
        '''
    )
    res = db.session.execute(query, {'user_id': user_id}).fetchall()
    return res if res else None

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
        SELECT c.name AS cat, i.name AS item,
        i.uom AS uom, g.quantity AS qty 
        FROM grocery_list_items g
        JOIN items i ON i.id=g.item_id
        JOIN categories c ON c.id=i.cat_id
        WHERE g.list_id=:list_id
        ORDER BY c.id, i.name
        '''
    )
    res = db.session.execute(query, {'list_id': list_id}).fetchall()

    groceries = {}
    for cat, item, uom, qty in res:
        if cat not in groceries:
            groceries[cat] = []
        groceries[cat].append((item, qty, uom))

    return groceries

def new_list(user_id, list_name=None):
    '''Create a new entry in the database and
    return the identifier of the new list.
    '''
    created_at = datetime.now(timezone.utc).strftime(
        '%Y-%m-%d %H:%M:%S%z'
    )[:-2]
    if not list_name:
        list_name = f'grocery list {created_at}'

    share_id = token_urlsafe(16)

    query = text(
        '''
        INSERT INTO grocery_list (user_id, created_at, name, share_id)
        VALUES (:user_id, :created_at, :name, :share_id)
        '''
    )
    db.session.execute(
        query,
        {'user_id': user_id, 'created_at': created_at,
         'name': list_name, 'share_id': share_id
        }
    )
    db.session.commit()

    query = text(
        '''
        SELECT id FROM grocery_list
        WHERE user_id=:user_id
        AND name=:name
        ORDER BY created_at DESC
        '''
    )
    list_id = db.session.execute(query, {'user_id': user_id, 'name': list_name}).fetchone()

    return list_id[0] if list_id else None

def _update_item(list_id, item_id, qty):
    '''Update the quantity of an item in an existing list.'''
    query = text(
        '''
        INSERT INTO grocery_list_items (list_id, item_id, quantity)
        VALUES (:list_id, :item_id, :qty)
        ON CONFLICT (item_id, list_id)
        DO UPDATE SET quantity=:qty
        '''
    )

    db.session.execute(query, {'list_id': list_id, 'item_id': item_id, 'qty': qty})
    db.session.commit()

def _delete_item(list_id, item_id):
    '''Delete an item from an existing list.'''
    query = text(
        '''
        DELETE FROM grocery_list_items
        WHERE item_id=:item_id AND list_id=:list_id
        '''
    )
    db.session.execute(query, {'list_id': list_id, 'item_id': item_id})
    db.session.commit()

def update_list_items(list_id, items, deleted=None):
    '''Update an existing grocery list.'''

    for item in items:
        item_id = get_item_id(item)
        _update_item(list_id, item_id, item['quantity'])

    if deleted:
        for item_id in deleted:
            _delete_item(list_id, item_id)

def update_list_name(list_id, list_name):
    query = text('UPDATE grocery_list SET name=:list_name WHERE id=:list_id')
    db.session.execute(query, {'list_name': list_name, 'list_id': list_id})
    db.session.commit()

def delete_list(list_id):
    '''Delete an existing list from database.'''
    query = text('DELETE FROM grocery_list WHERE id=:list_id')
    db.session.execute(query, {'list_id': list_id})
    db.session.commit()

def check_authorisation(user_id, list_id):
    '''Check if an user has access to a list.'''
    query = text(
        '''
        SELECT user_id FROM grocery_list
        WHERE id=:list_id AND user_id=:user_id
        '''
    )
    auth = db.session.execute(
        query, {'list_id': list_id, 'user_id': user_id}
    ).fetchone()

    return True if auth else False

def share_list(share_id):
    '''Get the list identifier and username of the
    user who created the list.
    '''
    query = text(
        '''
        SELECT u.username, g.id AS list_id
        FROM grocery_list g
        JOIN users u ON g.user_id=u.id
        WHERE g.share_id=:share_id
        '''
    )
    res = db.session.execute(
        query, {'share_id': share_id}
    ).fetchone()
    return res.username, res.list_id
