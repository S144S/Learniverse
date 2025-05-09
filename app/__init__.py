from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from .db_helper import DBHelper, UserManagement

app = Flask(__name__)
app.secret_key = "super_secret_key"

db = DBHelper()
    
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

from app import routes
