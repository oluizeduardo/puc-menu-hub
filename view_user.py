import constants
import utils
from flask import render_template, request, redirect
from models import User, Restaurant
from app import app, db


###################
# ROUTE ADD USER
###################
@app.route(constants.ID_ROUTE_USER, methods=["POST", "GET"])
def add_user():

    if request.method == 'POST':

        user = User(name=request.form['name'],
                    email=request.form['email'],
                    restaurant_id=request.form['restaurant'])
        user.set_password(request.form['password'])

        try:          
            utils.save_in_database(db, user)          
            return redirect(constants.ID_ROUTE_LOGIN)
        except:
            print(constants.MESSAGE_ERROR_SAVING_USER)
            return redirect(constants.ID_ROUTE_LOGIN)
    else:
        restaurants = Restaurant.query.all()
        return render_template(constants.ID_PAGE_USER, list_of_restaurants=restaurants)