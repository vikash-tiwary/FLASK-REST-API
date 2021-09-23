from api.models.users_models import db

class Post(db.Model):
    """
    Post model for post table
    id is a primary key
    """
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __init__(self,title,description):
        self.title=title
        self.description=description

class Author(db.Model):
    """
    Author model for author table
    id is primary key
    post id is a foreignkey
    """
    id = db.Column(db.Integer,primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    name = db.Column(db.String(100))
    
    def __init__(self,post_id,name):
        self.post_id=post_id
        self.name=name

class Address(db.Model):
    """
    Address model for address table
    id is primary key
    author id is a foreign key
    """
    id = db.Column(db.Integer,primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    details = db.Column(db.String(500))
    def __init__(self,author_id,details):
        self.author_id=author_id
        self.details=details
    
