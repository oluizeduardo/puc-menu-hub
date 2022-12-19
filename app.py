# required packages.
import os
import constants

from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# application setup.
# caminho absoluto da pasta do projeto.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, constants.DATABASE_NAME)}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


###################
# Class Model Plate
###################
class Plate(db.Model):
    __tablename__ = constants.PLATES_TABLE_NAME

    id       = db.Column(db.Integer, primary_key = True)
    name     = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(200), nullable = False)
    price    = db.Column(db.String(5), nullable = False)

    def __repr__(self):
        return f'Plate [#{self.id}, name: {self.name}, category: {self.category}, price: {self.price}]'

###################
# Class Model User
###################
class User(db.Model):
    __tablename__ = constants.USERS_TABLE_NAME

    id       = db.Column(db.Integer, primary_key = True)
    name     = db.Column(db.String(100), nullable = False)
    email    = db.Column(db.String(200), nullable = False)
    password = db.Column(db.String(5), nullable = False)

    def __repr__(self):
        return f'User [#{self.id}, name: {self.name}, email: {self.email}]'

###################
# LOGIN
###################
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':

        # Get parameters from the request.
        email = request.form['email']
        password = request.form['password']

        # Find user by email.
        found_user = User.query.filter_by(email=email).first()

        # Check email and password with the user's credentials.
        if email == found_user.email and password == found_user.password:
                # List the plates registered in the database.
                plates = Plate.query.order_by(Plate.name).all()
                return render_template(constants.ID_INDEX_PAGE, plates=plates)
        else:
            return render_template(constants.ID_LOGIN_PAGE)
    else:
        return render_template(constants.ID_LOGIN_PAGE)


###################
# ROUTE HOME
###################
@app.route("/home", methods=["POST", "GET"])
def home():
    if request.method == 'POST':

        plate = Plate(name=request.form['name'],
                      category=request.form['category'],
                      price=request.form['price'])
        try:           
            db.session.add(plate)
            db.session.commit()
            return redirect('/home')
        except:
            return constants.MESSAGE_ERROR_SAVING_PLATE
    else:
        # List the plates registered in the database.
        plates = Plate.query.order_by(Plate.name).all()
        return render_template(constants.ID_INDEX_PAGE, plates=plates)


###################
# ROUTE SEARCH
###################
@app.route("/search", methods=["POST", "GET"])
def search():
    return render_template(constants.ID_SEARCH_PAGE)


###################
# ROUTE ADD USER
###################
@app.route("/user/add", methods=["POST", "GET"])
def add_user():

    if request.method == 'POST':

        user = User(name=request.form['name'],
                      email=request.form['email'],
                      password=request.form['password'])
        try:
            # Insert a new user.            
            db.session.add(user)
            db.session.commit()            
            return redirect('/login')
        except:
            return constants.MESSAGE_ERROR_SAVING_USER
    else:
        return render_template(constants.ID_ADD_USER_PAGE)