'''Module for user account functions.'''
import re

from flask import session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

def login(username, password, err=list()):
    '''Check user credentials for logging in.

    param:
        username: str: name of the registered user
        password: str: password of the registered user
        err: list: list of errors (default: empty list)
    return:
        tuple: login success and list of errors
    '''

    logged_in = False
    query = text(
        '''
        SELECT id, password FROM users
        WHERE username=:username AND activated=TRUE
        '''
    )
    res = db.session.execute(query, {'username': username}).fetchone()
    user = res if res else None

    if user:
        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = username
            logged_in = True
        else:
            err.append('wrong_password')
    else:
        err.append('user_not_found')

    return (logged_in, err)

def logout():
    '''Log user out and clear session.'''
    session.clear()

def register(username, password):
    '''Register new user.

    param:
        username: str: name of the new user
        password: str: password for the new account
    return:
        tuple: registration success and list of errors
    '''
    def valid_username(username, min_length=3, max_length=16):
        if len(username) < min_length or len(username) > max_length:
            return False
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return False
        return True

    def valid_password(password, min_length=6, max_length=32):
        if len(password) < min_length or len(password) > max_length:
            return False
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]+$', password):
            return False
        return True

    registered = False
    err = []

    if not valid_username(username):
        err.append('invalid_username')

    if not valid_password(password):
        err.append('invalid_password')

    if not err:
        hashed_pw = generate_password_hash(password)
        try:
            query = text('INSERT INTO users (username, password) VALUES (:username, :password)')
            db.session.execute(query, {'username': username, 'password': hashed_pw})
            db.session.commit()
            registered, err = login(username, password, err=err)
        except IntegrityError:
            err.append('username_already_exists')

    return (registered, err)

def delete_account(user_id, password):
    '''Hides the user account from database and logs the user out,
    returning a boolean value depending on whether the operation
    was successful.
    '''
    query = text('SELECT password FROM users WHERE id=:user_id')
    hashed_pw = db.session.execute(query, {'user_id': user_id}).fetchone()[0]

    if check_password_hash(hashed_pw, password):
        query = text('UPDATE users SET activated=FALSE WHERE id=:user_id')
        db.session.execute(query, {'user_id': user_id})
        db.session.commit()
        logout()
        return True

    return False

def get_user_id():
    '''Return the user id used in the current session.'''
    return session.get('user_id', 0)

def get_username():
    '''Return the username used in the current session.'''
    return session.get('username', 0)
