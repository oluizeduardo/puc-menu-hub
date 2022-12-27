import constants
from flask import render_template, request, redirect
from models import User, Plate, Restaurant
from app import app, db

###################
# ROUTE LOGIN
###################
@app.route("/login", methods=["POST", "GET"])
def login():

    # List of all restaurants.
    restaurants = Restaurant.query.all()

    # The error message.
    error = None

    # Check the HTTP method.
    if request.method == 'POST':

        # Get parameters from the request.
        email = request.form['email']
        password = request.form['password']
        restaurant_id = request.form['restaurant_id']

        # Find user by email.
        user = User.query.filter_by(email=email).first()

        if user == None:
            error = constants.MESSAGE_ERROR_INVALID_CREDENTIALS
            # Render the login page if any user was found.
            return render_template(constants.ID_LOGIN_PAGE, list_of_restaurants=restaurants, error=error)
        
        else:
            # Check the password and the restaurant associaded to this user.
            if user.check_password(password) and user.check_restaurant_id(restaurant_id):

                # List the plates registered in the database.
                plates = Plate.query.order_by(Plate.name).all()
                return render_template(constants.ID_PLATES_PAGE, plates=plates)

            else:
                error = constants.MESSAGE_ERROR_INVALID_CREDENTIALS
                # Render the login page if the password doesn't match.
                return render_template(constants.ID_LOGIN_PAGE, list_of_restaurants=restaurants, error=error)
            
    else:
        # Render the login page if the HTTP method is not POST.
        return render_template(constants.ID_LOGIN_PAGE, list_of_restaurants=restaurants, error=error)


###################
# ROUTE PLATES
###################
@app.route("/plates", methods=["POST", "GET"])
def home():
    if request.method == 'POST':

        plate = Plate(name=request.form['name'],
                      category=request.form['category'],
                      price=request.form['price'],
                      restaurant_id=1)
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
                    restaurant_id=request.form['restaurant'])
        user.set_password(request.form['password'])

        try:
            # Insert a new user.            
            db.session.add(user)
            db.session.commit()            
            return redirect('/login')
        except:
            return constants.MESSAGE_ERROR_SAVING_USER
    else:
        restaurants = Restaurant.query.all()
        return render_template(constants.ID_ADD_USER_PAGE, list_of_restaurants=restaurants)


#######################
# ROUTE ADD RESTAURANT
#######################
@app.route("/addrestaurant", methods=["POST", "GET"])
def add_restaurant():

    if request.method == 'POST':

        restaurant = Restaurant(name=request.form['name'].upper())

        try:
            # Insert a new restaurant.            
            db.session.add(restaurant)
            db.session.commit()       
            return redirect('/addrestaurant')
        except:
            return constants.MESSAGE_ERROR_SAVING_RESTAURANT
    else:
        # List all the restaurants in the database.
        restaurants = Restaurant.query.order_by(Restaurant.id).all()
        return render_template(constants.ID_ADD_RESTAURANT_PAGE, restaurants=restaurants)