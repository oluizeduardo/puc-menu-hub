import constants
from app import db

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
        return f'User [#{self.id}, name: {self.name}, email: {self.email}, password: {self.password}]'
