from flask import Flask
from flask_bcrypt import Bcrypt
from .db_helper import DBHelper

app = Flask(__name__)
app.secret_key = "super_secret_key"

db = DBHelper()
    
bcrypt = Bcrypt(app)

from app import routes
