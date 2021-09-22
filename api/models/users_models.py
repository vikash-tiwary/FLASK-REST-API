from flask_sqlalchemy import SQLAlchemy 
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY']= 'thisissecret'

"""
MYSQL database 
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/post'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

db = SQLAlchemy(app)

class User(db.Model):
    """
    User model for user table
    id is a primary key
    public id is a unique key
    """
    id=db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(200))
    password=db.Column(db.String(500))
    admin=db.Column(db.Boolean)
