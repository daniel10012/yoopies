from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a new Flask application
app = Flask(__name__)

# Set up SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sh14.db'
db = SQLAlchemy(app)

# Define a class for the Artist table
class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    CODGEO = db.Column(db.Integer)


# Create the table
# db.create_all()