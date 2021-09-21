# FLASK-REST-API

# Requirements
--------------
Create a REST API in python flask with GET, POST, PUT, DELETE methods
1. Use mysql as database along with SQLalchemy
2. It should follow the MVC pattern - model-view-controller
3. The project should contain atleast 4 tables and include joins
4. The API endpoints should not be accessible, can be accessed only with security token
5. Create unit/functional test cases

# Data Base Creation
I have created post database in mysql-db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/post'

~/project/FLASK-REST-API$ python
>>> from api.models import db
>>>db.create_all()

In this Project I have taken 4 table
All three post,author and address table is connected with foreign key
1. User Model

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50),unique=True)
    name=db.Column(db.String(200))
    password=db.Column(db.String(500))
    admin=db.Column(db.Boolean)

2. Post
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))

3. Author
class Author(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    name = db.Column(db.String(100))

4. Addresss

class Address(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    details = db.Column(db.String(500))