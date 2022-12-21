import os
import constants

from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, constants.DATABASE_NAME)}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

bootstrap = Bootstrap5(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from views import *