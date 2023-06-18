from flask import redirect, render_template, request, url_for

from app import app
import groceries
import users

@app.before_request
def before_request():
    authorised = ['index', 'login', 'register']
    endpoint = request.endpoint
    user_id = users.get_user_id()
    username = users.get_username()

    if endpoint in authorised:
        return

    if not user_id:
        return redirect(url_for('login'))
    elif username not in endpoint:
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
            return redirect('/error', message=msg, prev=url_for('login'))

    return render_template('login.html')

@app.route('/error')
def error(message=None, prev=None):
    if not message:
        message = 'unidentified_error'
    if not prev:
        prev = url_for('index')
    return render_template('error.html', message, prev)

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
            return redirect('/error', message='password_does_not_match', prev=url_for('register'))

        registered, err = users.register(username, password)
        if not registered:
            msg = ', '.join(err)
            return redirect('/error', message=msg, prev=url_for('register'))

    return render_template('register.html')

@app.route('/profile/<string:username>')
def profile(username):
    if username != users.get_username():
        return redirect('/error', message='unauthorised')
    return render_template('profile.html')

@app.route('/new_list')
def new_list():
    categories = groceries.get_category_dict().keys
    return render_template('new_list.html', categories=categories)

@app.route('/submit_list', methods=['POST'])
def submit_list():
    user_id = users.get_user_id()
    categories = groceries.get_category_dict()
    list_name = request.form['list_name']
    items = []
    names = request.form.getlist('item_name[]')
    qtys = request.form.getlist('quantity[]')
    uoms = request.form.getlist('uom[]')
    cats = request.form.getlist('category[]')

    for name, qty, uom, cat in zip(names, qtys, uoms, cats):
        item = {
            'name': name,
            'quantity': qty,
            'uom': uom,
            'category': categories[cat]
        }
        items.append(item)

    list_id = groceries.new_list(user_id, list_name)

@app.route('/lists/<int:list_id>')
def lists(list_id):
    pass
