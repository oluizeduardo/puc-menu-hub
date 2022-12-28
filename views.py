import constants
from flask import render_template, request, redirect
from models import User, Plate, Restaurant
from app import app, db, session

###################
# ROUTE LOGIN
###################
@app.route("/login", methods=["POST", "GET"])
def login():

    # Check the HTTP method.
    if request.method == 'POST':

        # Get parameters from the request.
        email = request.form['email']
        password = request.form['password']
        restaurant_id = request.form['restaurant_id']

        # Find user by email.
        user = User.query.filter_by(email=email).first()

        if user:
            # Check the password and the restaurant id associaded to this user.
            if user.check_password(password) and user.check_restaurant_id(restaurant_id):

                # Add user to session.
                session[constants.SESSION_ID] = user

                # Redirect to home page '/plates'.
                return redirect('/plates')

            else:
                # Stay in the login page if the password doesn't match.
                return render_login_page(constants.MESSAGE_ERROR_INVALID_CREDENTIALS) 
        else:
            # Stay in the login page if any user was found.
            return render_login_page(constants.MESSAGE_ERROR_INVALID_CREDENTIALS) 
    else:
        # Stay in the login page if the HTTP method is not POST.
        return render_login_page(None)


###################
# ROUTE LOGOUT
###################
@app.route("/logout", methods=["POST", "GET"])
def logout():

    message = None

    if not is_empty_session():
        # Clean session.
        session[constants.SESSION_ID] = None
        message = constants.MESSAGE_LOG_OUT

    return render_login_page(message)          


###################
# ROUTE PLATES
###################
@app.route("/plates", methods=["POST", "GET"])
def home():
    
    if is_empty_session():
        return render_login_page(constants.MESSAGE_PLEASE_LOG_IN)

    # Get the user's restaurant id.
    logged_user_restaurant_id = get_restaurant_id_from_logged_user()

    if request.method == 'POST':

        plate = Plate(name=request.form['name'],
                      category=request.form['category'],
                      price=request.form['price'],
                      restaurant_id = logged_user_restaurant_id)
        try:           
            save_in_database(plate)
            return redirect('/plates')
        except:
            print(constants.MESSAGE_ERROR_SAVING_PLATE)
            return redirect('/plates')
    else:
        plates = get_plates_of_logged_user_restaurant(logged_user_restaurant_id)
        return render_template(constants.ID_PLATES_PAGE, plates=plates)


###################
# ROUTE SEARCH
###################
@app.route("/search", methods=["POST", "GET"])
def search():
    if is_empty_session():
        return render_login_page(constants.MESSAGE_PLEASE_LOG_IN)
    
    plates = None

    if request.method == 'POST':

        plate_id = request.form.get('plate_id')
        plate_name = request.form.get('plate_name')
        
        if plate_id:
            plates = Plate.query.filter(Plate.id == plate_id).all()

        if plate_name:
            plates = Plate.query.filter(Plate.name == plate_name).order_by(Plate.restaurant_id).all()
    else:
        plates = Plate.query.order_by(Plate.id).all()
    
    return render_template(constants.ID_SEARCH_PAGE, plates=plates)


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
            save_in_database(user)          
            return redirect('/login')
        except:
            print(constants.MESSAGE_ERROR_SAVING_USER)
            return redirect('/login')
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
            save_in_database(restaurant)      
            return redirect('/addrestaurant')
        except:
            print(constants.MESSAGE_ERROR_SAVING_RESTAURANT)
            return redirect('/addrestaurant')
    else:
        # List all the restaurants in the database.
        restaurants = Restaurant.query.order_by(Restaurant.id).all()
        return render_template(constants.ID_ADD_RESTAURANT_PAGE, restaurants=restaurants)


def is_empty_session():
    return constants.SESSION_ID not in session or session[constants.SESSION_ID] == None


def render_login_page(message):
    # List of all restaurants.
    restaurants = Restaurant.query.all()
    return render_template(constants.ID_LOGIN_PAGE, list_of_restaurants=restaurants, message=message)

""" 
Return the user's restaurant id.
"""
def get_restaurant_id_from_logged_user():
    user = session.get(constants.SESSION_ID)
    return user.restaurant_id

""" 
Return a list of plates registered for the user's restaurant.
"""
def get_plates_of_logged_user_restaurant(logged_user_restaurant_id):
    return Plate.query.filter(Plate.restaurant_id == logged_user_restaurant_id).all()


def save_in_database(model_object):
    db.session.add(model_object)
    db.session.commit()