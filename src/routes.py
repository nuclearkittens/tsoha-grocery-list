from flask import redirect, render_template, request, url_for

from app import app
import users

@app.route('/')
def index():
    '''Render the main page.'''
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Render the login page or related error pages.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        logged_in, err = users.login(username, password)
        if not logged_in:
            msg = ', '.join(err)
            return render_template('error.html', message=msg, prev=url_for('login'))

    return render_template('login.html')

@app.route('/error')
def error():
    return render_template('error.html', message='unidentified_error', prev=url_for('index'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        users.logout()
    return render_template('logout.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Render the registration page or related errors.'''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_check = request.form['password_check']
        if password != password_check:
            return render_template('error.html', message='password_does_not_match', prev=url_for('register'))

        registered, err = users.register(username, password)
        if not registered:
            msg = ', '.join(err)
            return render_template('error.html', message=msg, prev=url_for('register'))

    return render_template('register.html')
