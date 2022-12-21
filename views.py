import constants
from flask import render_template, request, redirect
from models import User, Plate
from app import app, db

###################
# ROUTE LOGIN
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
                return render_template(constants.ID_PLATES_PAGE, plates=plates)
        else:
            return render_template(constants.ID_LOGIN_PAGE)
    else:
        return render_template(constants.ID_LOGIN_PAGE)


###################
# ROUTE HOME
###################
@app.route("/plates", methods=["POST", "GET"])
def home():
    if request.method == 'POST':

        plate = Plate(name=request.form['name'],
                      category=request.form['category'],
                      price=request.form['price'])
        try:           
            db.session.add(plate)
            db.session.commit()
            return redirect('/plates')
        except:
            return constants.MESSAGE_ERROR_SAVING_PLATE
    else:
        # List the plates registered in the database.
        plates = Plate.query.order_by(Plate.id).all()
        return render_template(constants.ID_PLATES_PAGE, plates=plates)


###################
# ROUTE SEARCH
###################
@app.route("/search", methods=["POST", "GET"])
def search():
    return render_template(constants.ID_SEARCH_PAGE)


###################
# ROUTE ADD USER
###################
@app.route("/adduser", methods=["POST", "GET"])
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