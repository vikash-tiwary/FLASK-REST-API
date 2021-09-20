from flask_sqlalchemy import SQLAlchemy 
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY']= 'thisissecret'


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/post'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(200))
    password=db.Column(db.String(500))
    admin=db.Column(db.Boolean)

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    author = db.Column(db.String(100))

    def __init__(self,title,author,description):
        self.title=title
        self.description=description
        self.author=author

class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    name = db.Column(db.String(100))

class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    description = db.Column(db.String(500))
    
