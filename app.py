# required packages.
import os

from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# application setup.
# caminho absoluto da pasta do projeto.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(basedir, 'menuhub.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Class model.
class Plate(db.Model):
    __tablename__ = "plates"

    id       = db.Column(db.Integer, primary_key = True)
    name     = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(200), nullable = False)
    price    = db.Column(db.String(5), nullable = False)

    def __repr__(self):
        return f'Plate [#{self.id}, name: {self.name}, category: {self.category}, price: {self.price}]'


# applications routes.
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':

        plate = Plate(name=request.form['name'],
                      category=request.form['category'],
                      price=request.form['price'])
        try:
            # Insert a new plate.            
            db.session.add(plate)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error trying to save the plate."
        
    else:
        # List the plates registered in the database.
        plates = Plate.query.order_by(Plate.name).all()
        return render_template('index.html', plates=plates)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if email == 'teste@email.com' and password == 'abc123':
                # List the plates registered in the database.
                plates = Plate.query.order_by(Plate.name).all()
                return render_template('index.html', plates=plates)
        else:
            return render_template('login.html')
        
    else:
        return render_template('login.html')


@app.route("/search", methods=["POST", "GET"])
def search():
    return render_template('search.html')