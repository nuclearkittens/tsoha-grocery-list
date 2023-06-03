'''Module for user account functions.'''

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

def login(username, password):
    '''Check user credentials for logging in.

    param:
        username (str): name of the registered user
        password (str): password of the registered user
    return:
        bool: login successful
    '''
    sql = 'SELECT id, password FROM users WHERE username=:username'
    user = db.session.execute(sql, {'username': username}).fetchone()

    try:
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            return True
        else:
            print('login error: wrong password')
    except:
        print('login error: user not found')

    return False

def logout():
    '''Log user out and clear session.'''
    session.clear()

def register(username, password):
    # TODO: username/pw constraints
    '''Register new user.

    param:
        username (str): name of the new user
        password (str): password for the new account
    return:
        bool: successful login to new account.
    '''
    hashed_pw = generate_password_hash(password)
    sql = 'INSERT INTO users (username, password) VALUES (:username, :password)'
    db.session.execute(sql, {'username': username, 'password': hashed_pw})
    db.session.commit()
    return login(username, password)

def get_user_id():
    '''Return the user id used in the current session.'''
    return session.get('user_id', 0)
