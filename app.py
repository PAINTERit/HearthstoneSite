from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.debug = True

UPLOAD_FOLDER = 'static/user_image'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024

app.config['SECRET_KEY'] = 'jwdjdwkjdwkdwkdw'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
toolbar = DebugToolbarExtension(app)

db = SQLAlchemy(app)
manager = LoginManager(app)
toastr = Toastr(app)
app.config['TOASTR_SHOW_METHOD'] = 'show'
app.config['TOASTR_TIMEOUT'] = 5000

