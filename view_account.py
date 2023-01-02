import constants
import utils
from flask import request, redirect
from models import User
from app import app, session


###################
# ROUTE LOGIN
###################
@app.route(constants.ID_ROUTE_LOGIN, methods=["POST", "GET"])
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
                return redirect(constants.ID_ROUTE_PLATES)

            else:
                # Stay in the login page if the password doesn't match.
                return utils.render_login_page(constants.MESSAGE_ERROR_INVALID_CREDENTIALS) 
        else:
            # Stay in the login page if any user was found.
            return utils.render_login_page(constants.MESSAGE_ERROR_INVALID_CREDENTIALS) 
    else:
        # Stay in the login page if the HTTP method is not POST.
        return utils.render_login_page(None)


###################
# ROUTE LOGOUT
###################
@app.route(constants.ID_ROUTE_LOGOUT, methods=["POST", "GET"])
def logout():

    message = None

    if not utils.is_empty_session():
        # Clean session.
        session[constants.SESSION_ID] = None
        message = constants.MESSAGE_LOG_OUT
    return utils.render_login_page(message)