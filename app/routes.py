from app import app
from flask import render_template

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/')
def home():
    return render_template('layout.html')

# @app.route('/mission')
# def mission():
#     return render_template('mission.html')

# @app.route('/planet')
# def planet():
#     return render_template('planet.html')
