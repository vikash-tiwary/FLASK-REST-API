from flask_marshmallow import Marshmallow
from api.models import app
ma = Marshmallow(app)

class PostSchema(ma.Schema):
    class Meta:
        fields=["title","author","description"]

post_schema = PostSchema()
posts_schema = PostSchema(many=True)


class AuthorSchema(ma.Schema):
    class Meta:
        fields=["post_id","name"]

auth_schema = AuthorSchema()
auths_schema = AuthorSchema(many=True)


class AddressSchema(ma.Schema):
    class Meta:
        fields=["author_id","details"]

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)
