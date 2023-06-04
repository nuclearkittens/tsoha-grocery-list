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
            # TODO: display correct error when failed login
            msg = ', '.join(err)
            return render_template('error.html', message=msg, prev=url_for('login'))

    return render_template('login.html')

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
            return render_template('error.html', message='passwords don\'t match ):')

        registered, err = users.register(username, password)
        if not registered:
            # TODO: display correct error when failed registration
            msg = ', '.join(err)
            return render_template('error.html', message=msg, prev=url_for('register'))

    return render_template('register.html')
