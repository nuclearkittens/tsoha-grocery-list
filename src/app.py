'''Module for initialising the application.'''

from os import getenv
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from db import init_db

app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
csrf = CSRFProtect(app)
init_db(app)

import routes
