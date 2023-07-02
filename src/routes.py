from flask import redirect, render_template, request, url_for

from app import app
import groceries
import users

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

@app.route('/delete_account')
def delete_account():
    '''Display the account deletion form.'''
    user_id = users.get_user_id()

    if not user_id:
        redirect(url_for('error', message='unauthorised'))

    return render_template('delete_account.html')

@app.route('/delete_account_check', methods=['POST'])
def delete_account_check():
    '''Delete the user account.'''
    user_id = users.get_user_id()
    password = request.form.get('password')
    confirm = request.form.get('confirm')

    deleted = False
    if confirm == 'on':
        deleted = users.delete_account(user_id, password)

    return render_template('delete_account_confirmation.html', deleted=deleted)

@app.route('/profile/<string:username>', methods=['GET', 'POST'])
def profile(username):
    '''Render the profile page of the user.'''
    if username != users.get_username():
        return redirect(url_for('error', message='unauthorised'))

    user_id = users.get_user_id()
    grocery_lists = groceries.get_lists_by_user(user_id)

    return render_template('profile.html', grocery_lists=grocery_lists)

@app.route('/new_list')
def new_list():
    '''Render the form for creating a new shopping list.'''
    if not users.get_user_id():
        return redirect(url_for('login'))

    categories = groceries.get_category_dict().keys()
    return render_template('new_list.html', categories=categories)

@app.route('/submit_list', methods=['POST'])
def submit_list():
    '''Save the newly created list to the database and
    redirect user to the list's page.'''
    user_id = users.get_user_id()
    categories = groceries.get_category_dict()
    list_name = request.form['list_name']

    names = request.form.getlist('item_name[]')
    qtys = request.form.getlist('quantity[]')
    uoms = request.form.getlist('uom[]')
    cats = request.form.getlist('category[]')

    items = []
    for name, qty, uom, cat in zip(names, qtys, uoms, cats):
        item = {
            'name': name,
            'quantity': qty,
            'uom': uom,
            'category': categories[cat]
        }
        items.append(item)

    list_id = groceries.new_list(user_id, list_name)
    groceries.update_list_items(list_id, items)

    return redirect(url_for('lists', list_id=list_id))

@app.route('/edit_list')
def edit_list():
    '''Edit an existing grocery list.'''
    user_id = users.get_user_id()
    list_id = request.args.get('list_id')
    categories = groceries.get_category_dict()

    if groceries.check_authorisation(user_id, list_id):
        list_items = groceries.get_list_items(list_id)
        list_name, _, _ = groceries.get_list_info(list_id)
        return render_template(
            'edit_list.html', list_id=list_id, list_name=list_name,
            list_items=list_items, categories=categories,
            item_count=len(list_items)
        )

    return redirect(url_for('error', message='unauthorised'))

@app.route('/submit_edits', methods=['POST'])
def submit_edits():
    '''Save the changes in the database and
    redirect user to the list's page.'''
    categories = groceries.get_category_dict()
    list_name = request.form['list_name']
    list_id = request.form['list_id']

    names = request.form.getlist('item_name[]')
    qtys = request.form.getlist('quantity[]')
    uoms = request.form.getlist('uom[]')
    cats = request.form.getlist('category[]')
    deleted = request.form.getlist('deleted[]')

    items = []
    for name, qty, uom, cat in zip(names, qtys, uoms, cats):
        item = {
            'name': name,
            'quantity': qty,
            'uom': uom,
            'category': categories[cat]
        }
        items.append(item)

    groceries.update_list_items(list_id, items, deleted)
    groceries.update_list_name(list_id, list_name)

    return redirect(url_for('lists', list_id=list_id))

@app.route('/delete_list')
def delete_list():
    '''Display the list deletion page.'''
    user_id = users.get_user_id()
    list_id = request.args.get('list_id')

    if groceries.check_authorisation(user_id, list_id):
        list_info = groceries.get_list_info(list_id)
        return render_template('delete_list.html', list_id=list_id, list_name=list_info[0])

    return redirect(url_for('error', message='unauthorised'))

@app.route('/delete_list_check', methods=['POST'])
def delete_list_check():
    '''Delete the specified list.'''
    list_id = request.form.get('list_id')
    confirm = request.form.get('confirm')

    if confirm == 'on':
        groceries.delete_list(list_id)
        return render_template('delete_list_confirmation.html', deleted=True)
    elif confirm != 'on':
        return render_template('delete_list_confirmation.html', deleted=False)
    else:
        return redirect(url_for('error', message='list_deletion_failed'))

@app.route('/lists')
def lists():
    '''Display the specified grocery list if the user
    has access rights.'''
    user_id = users.get_user_id()
    username = users.get_username()
    list_id = request.args.get('list_id')

    if groceries.check_authorisation(user_id, list_id):
        list_name, timestamp, share_id = groceries.get_list_info(list_id)
        list_items = groceries.get_sorted_list(list_id)
        return render_template(
            'lists.html', list_id=list_id, list_name=list_name, share_id=share_id,
            timestamp=timestamp, list_items=list_items, username=username
        )

    return redirect(url_for('error', message='unauthorised'))

@app.route('/shared')
def shared():
    '''Display a shared grocery list.'''
    share_id = request.args.get('share_id')
    username, list_id = groceries.share_list(share_id)
    list_name, timestamp, _ = groceries.get_list_info(list_id)
    list_items = groceries.get_sorted_list(list_id)
    return render_template(
            'lists.html', list_id=None, list_name=list_name,
            timestamp=timestamp, list_items=list_items, username=username
        )
