from flask import redirect, render_template, request

from app import app
from db import db
import users

@app.route('/')
def index():
    '''Render the main page.'''
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if users.login(username, password):
        return redirect('/')
    
    return render_template('index.html', error=True, errormsg='login failed ):')

@app.route('/logout')
def logout():
    users.logout()
    return render_template('logout.html')
