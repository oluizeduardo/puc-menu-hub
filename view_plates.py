import constants
import utils
from flask import render_template, request, redirect
from models import Plate
from app import app, db, session

###########################
# ROUTE ADD AND LIST PLATES
###########################
@app.route(constants.ID_ROUTE_PLATES, methods=["POST", "GET"])
def home():
    
    if utils.is_empty_session():
        return utils.render_login_page(constants.MESSAGE_PLEASE_LOG_IN)

    # Get the user's restaurant id.
    logged_user_restaurant_id = get_restaurant_id_from_logged_user()

    if request.method == 'POST':

        plate = Plate(name=request.form['name'].upper(),
                      category=request.form['category'],
                      price=float(request.form['price']),
                      restaurant_id = logged_user_restaurant_id)
        try:           
            utils.save_in_database(db, plate)
            return redirect(constants.ID_ROUTE_PLATES)
        except:
            print(constants.MESSAGE_ERROR_SAVING_PLATE)
            return redirect(constants.ID_ROUTE_PLATES)
    else:
        # Brings all the plates of the user's restaurant.
        plates = get_plates_of_logged_user_restaurant(logged_user_restaurant_id)
        return render_template(constants.ID_PAGE_PLATES, plates=plates)


#######################
# ROUT EDIT A PLATE
#######################
@app.route("/plates/edit", methods=["POST"])
def edit_plate():

    plate_id    = request.form['plateId']
    newName     = request.form['editedName'].upper()
    newCategory = request.form['editedCategory']
    newPrice    = request.form['editedPrice']

    try:
        plateToBeEdited = Plate.query.filter(Plate.id == int(plate_id)).first()

        if plateToBeEdited:
            plateToBeEdited.name = str(newName)
            plateToBeEdited.category = str(newCategory)
            plateToBeEdited.price = float(newPrice)
            db.session.flush()
            db.session.commit()
            db.session.close()
    except:
        print('[edit_plate]' + constants.MESSAGE_ERROR_EDITING_PLATE)

    return redirect(constants.ID_ROUTE_PLATES)


#######################
# ROUT DELETE A PLATE
#######################
@app.route("/plates/delete/<plate_id>", methods=["GET"])
def delete_plate(plate_id):    
    try:
        Plate.query.filter(Plate.id == int(plate_id)).delete()
        db.session.commit()
    except:
        print('[delete_plate] - ' + constants.MESSAGE_ERROR_DELETING_PLATE)
    return redirect(constants.ID_ROUTE_PLATES)


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