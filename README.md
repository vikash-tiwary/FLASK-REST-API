# FLASK-REST-API

## Requirements
--------------
Create a REST API in python flask with GET, POST, PUT, DELETE methods
1. Use mysql as database along with SQLalchemy
2. It should follow the MVC pattern - model-view-controller
3. The project should contain atleast 4 tables and include joins
4. The API endpoints should not be accessible, can be accessed only with security token
5. Create unit/functional test cases


### Set up emvironment
The installation is very streight forward 
and make sure that you are using python 3.8

```bash
$ cd FLASK-REST-API
$ virtualenv env
(env)$ source env/bin/actiavte
(env)FLASK-REST-API$ pip install -r requirements.txt

```
### Running

When all dependencies has been installed, You can run the flask application 
on local isnatance by running 

```bash
(env)FLASK-REST-API$ export FLASK_APP=app.py
(env)FLASK-REST-API$ flask run

```

### Data Base Creation
I have created post database in mysql-db

```bash
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:''@localhost/post'

~/project/FLASK-REST-API$ python
>>> from api.models import db
>>>db.create_all()

```

### Testing
when the database and application is created 
Then test file 

```bash
(env)FLASK-REST-API$ pytest test_post_model.py
(env)FLASK-REST-API$ pytest test_user_model.py
(env)FLASK-REST-API$ pytest test_post.py
(env)FLASK-REST-API$ pytest test_login.py
(env)FLASK-REST-API$ pytest test_author.py
(env)FLASK-REST-API$ pytest test_address.py
(env)FLASK-REST-API$ pytest test_users.py
```