# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    certificates = db.relationship('Certificate', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Certificate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(200))
    creation_date = db.Column(db.Date)
    valid_to_date = db.Column(db.Date)
    comments = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    zip_password = db.Column(db.String(255))
    pfx_password = db.Column(db.String(255))
