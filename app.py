"""
Модуль, хранящий константы и настройки модулей для проекта.
"""

import uuid

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_toastr import Toastr

app = Flask(__name__)
app.debug = True

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['TOASTR_SHOW_METHOD'] = 'show'
app.config['TOASTR_TIMEOUT'] = 5000
app.config['DEBUG'] = True
toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)
manager = LoginManager(app)
toastr = Toastr(app)
