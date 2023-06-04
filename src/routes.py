from flask import redirect, render_template, request

from app import app
import users

@app.route('/')
def index():
    '''Render the main page.'''
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        logged_in, _ = users.login(username, password)
        if not logged_in:
            # TODO: display correct error when failed login
            return render_template('error.html', message='login failed ):', prev='/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    users.logout()
    return render_template('logout.html')

@app.route('/register')
def register():
    return render_template('register.html')
