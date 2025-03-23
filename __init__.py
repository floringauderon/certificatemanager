# __init__.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from dotenv import load_dotenv
import os
import datetime
import sendgrid
from sendgrid.helpers.mail import Mail

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# SendGrid API key
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

from . import models  # Import models first, before routes

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

from . import routes  # Import routes after db and app creation.

if __name__ == '__main__':
    app.run(debug=True)