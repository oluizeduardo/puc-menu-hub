import constants
import utils
from flask import render_template, request
from models import Plate
from app import app


#####################
# ROUTE SEARCH PLATES
#####################
@app.route(constants.ID_ROUTE_SEARCH, methods=["POST", "GET"])
def search():
    if utils.is_empty_session():
        return utils.render_login_page(constants.MESSAGE_PLEASE_LOG_IN)
    
    plates = None
    message = None

    if request.method == 'POST':

        plate_id = request.form.get('plate_id')
        plate_name = request.form.get('plate_name')
        
        if plate_id:
            plates = Plate.query.filter(Plate.id == plate_id).all()

        if plate_name:
            plates = Plate.query\
                .filter(Plate.name == plate_name.upper())\
                .order_by(Plate.restaurant_id).all()
        
        if not plates:
            message = constants.MESSAGE_NOTHING_FOUND
    else:
        plates = Plate.query.order_by(Plate.id).all()

    return render_template(constants.ID_PAGE_SEARCH, plates=plates, message=message)