import constants
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.hybrid import hybrid_property
from app import db
from datetime import datetime

##########################
# Class Model Restaurant
##########################
class Restaurant(db.Model):
    __tablename__ = constants.RESTAURANTS_TABLE_NAME

    id     = db.Column(db.Integer, primary_key = True)
    name   = db.Column(db.String(100), nullable = False)
    plates = db.relationship('Plate', backref='restaurants', lazy="joined")
    users  = db.relationship('User',  backref='restaurants', lazy="joined")
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'Restaurant [#{self.id}, name: {self.name}, created_on: {self.created_on}]'

###################
# Class Model Plate
###################
class Plate(db.Model):
    __tablename__ = constants.PLATES_TABLE_NAME

    id         = db.Column(db.Integer, primary_key = True)
    name       = db.Column(db.String(100), nullable = False)
    category   = db.Column(db.String(200), nullable = False)
    price      = db.Column(db.String(5), nullable = False)    
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return f'Plate [#{self.id}, name: {self.name}, category: {self.category}, price: {self.price}, created_on: {self.created_on}]'

###################
# Class Model User
###################
class User(db.Model):
    __tablename__ = constants.USERS_TABLE_NAME

    id         = db.Column(db.Integer, primary_key = True)
    name       = db.Column(db.String(100), nullable = False)
    email      = db.Column(db.String(200), nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable = False)  
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    def check_email(self, email):
        return email == self.email

    def set_password(self, plainTextPassword):
        self.password_hash = generate_password_hash(plainTextPassword)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def check_restaurant_id(self, restaurant_id):
        return int(restaurant_id) == self.restaurant_id

    def __repr__(self):
        return f'User [#{self.id}, name: {self.name}, restaurant_id: {self.restaurant_id}, email: {self.email}, created_on: {self.created_on}]'
