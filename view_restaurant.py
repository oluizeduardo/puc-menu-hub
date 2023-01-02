import constants
import utils
from flask import render_template, request, redirect
from models import Restaurant
from app import app, db


#######################
# ROUTE ADD RESTAURANT
#######################
@app.route(constants.ID_ROUTE_RESTAURANT, methods=["POST", "GET"])
def add_restaurant():

    if request.method == 'POST':

        restaurant = Restaurant(name=request.form['name'].upper())

        try:           
            utils.save_in_database(db, restaurant)      
            return redirect(constants.ID_ROUTE_RESTAURANT)
        except:
            print(constants.MESSAGE_ERROR_SAVING_RESTAURANT)
            return redirect(constants.ID_ROUTE_RESTAURANT)
    else:
        # List all the restaurants in the database.
        restaurants = Restaurant.query.order_by(Restaurant.id).all()
        return render_template(constants.ID_PAGE_RESTAURANT, restaurants=restaurants)