from flask_marshmallow import Marshmallow
from app import app
ma = Marshmallow(app)

class PostSchema(ma.Schema):
    class Meta:
        fields=["title","author","description"]

post_schema = PostSchema()
posts_schema = PostSchema(many=True)
