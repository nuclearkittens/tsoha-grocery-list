from flask import redirect, render_template, request, url_for

from app import app
import groceries
import users

# @app.before_request
# def before_request():
#     authorised = ['index', 'login', 'login/check', 'register', 'register/check']
#     endpoint = request.endpoint
#     user_id = users.get_user_id()

#     if endpoint in authorised:
#         return
#     elif not user_id:
#         return redirect(url_for('login'))

#     return

@app.errorhandler(404)
def page_not_found(e):
    message = '404_page_not_found'
    return redirect(url_for('error', message=message))

@app.errorhandler(405)
def method_not_allowed(e):
    message = '405_method_not_allowed'
    return redirect(url_for('error', message=message))

@app.route('/')
def index():
    '''Render the main page.'''
    return render_template('index.html')

@app.route('/login')
def login():
    '''Render the login page'''
    return render_template('login.html')

@app.route('/login/check', methods=['POST'])
def login_check():
    '''Check if user is logged in.'''
    username = request.form['username']
    password = request.form['password']

    logged_in, err = users.login(username, password)
    if not logged_in:
        msg = ', '.join(err)
        return redirect(url_for('error', message=msg))

    return redirect(url_for('login'))

@app.route('/error')
def error():
    '''Render the error page with either a specified or
    general error message.'''
    message = request.args.get('message')

    if not message:
        message = 'unidentified_error'

    return render_template('error.html', message=message)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''Render the logout page.'''
    return render_template('logout.html')

@app.route('/logout/check', methods=['POST'])
def logout_check():
    '''Log user out.'''
    users.logout()
    return redirect(url_for('logout'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Render the registration page or related errors.'''
    return render_template('register.html')

@app.route('/register/check', methods=['POST'])
def register_check():
    '''Check the registration.'''
    username = request.form['username']
    password = request.form['password']
    password_check = request.form['password_check']
    print(username, password, password_check)
    if password != password_check:
        return redirect(url_for(
            'error', message='password_does_not_match'
        ))

    registered, err = users.register(username, password)
    print(registered, err)
    if not registered:
        msg = ', '.join(err)
        return redirect(url_for('error', message=msg))

    return redirect(url_for('register'))

@app.route('/profile/<string:username>', methods=['GET', 'POST'])
def profile(username):
    if username != users.get_username():
        return redirect(url_for('error', message='unauthorised'))
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
