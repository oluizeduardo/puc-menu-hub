import os
import constants

from flask_session import Session
from flask_bootstrap import Bootstrap5
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, constants.DATABASE_NAME)}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from view_account import *
from view_plates import *
from view_search import *
from view_user import *
from view_restaurant import *