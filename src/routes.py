from flask import redirect, render_template, request, url_for

from app import app
import users

@app.before_request
def before_request():
    authorised = ['index', 'login', 'register']
    endpoint = request.endpoint
    user_id = users.get_user_id()

    if endpoint in authorised:
        return

    if not user_id:
        return redirect(url_for('login'))
    elif '/profile' in endpoint and user_id not in endpoint:
        return render_template('error.html', message='unauthorised', prev=url_for('index'))

    return


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

@app.route('/profile/<string:username>')
def profile(username):
    return render_template('profile.html')

@app.route('/new_list')
def new_list():
    return render_template('new_list.html')
