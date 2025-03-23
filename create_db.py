# create_db.py
import sys
import os

# Set the parent_dir
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add it to sys.path just to be sure
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
# Imports
from mysite import app, db
from mysite import models

# Create the talbes
with app.app_context():
    db.create_all()
    print("Database tables created!")
