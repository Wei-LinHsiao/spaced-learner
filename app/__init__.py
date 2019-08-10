# Flask Imports
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Configure the app.
app = Flask(__name__)
app.config.from_object(Config)

# Set up logins.
login = LoginManager(app)

# Set up the database.
db = SQLAlchemy(app)
from app import models
# Change box creation to store essential parameters, such as unque id.
db.drop_all()
db.create_all()

# Set up leitner box logic.
from app import leitner_boxes

current_box = leitner_boxes.BoxSet(0)

# Mock db of all entires; list for now.
if app.config["TEST"]:
    current_box.create_entry("One", "")
    current_box.create_entry("Two", "")
    current_box.create_entry("Three", "")
    current_box.create_entry("Four", "")
    current_box.create_entry("Five", "")
    current_box.create_entry("Six", "")
    current_box.create_entry("Seven", "")

# Set up routes.
from app import routes

