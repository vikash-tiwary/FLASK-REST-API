from os import name
from flask import Flask ,request,jsonify,session,Blueprint
import jwt
import datetime
from api.models.post_models import Post
from api.schema.post_schema import post_schema,posts_schema
import uuid
from api.controllers.login import token_required
from api.models.users_models import db

post_blueprint = Blueprint('post', __name__,url_prefix='/post')


@post_blueprint.route('/post',methods=['POST'])
@token_required
def add_post(current_user):
    """
    This function is use to create new post in database
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    data=request.get_json(force=True)

    title=data['title']
    description=data['description']

    my_posts=Post(title=title,description=description)

    db.session.add(my_posts)
    db.session.commit()

    return post_schema.jsonify(my_posts)


@post_blueprint.route('/get', methods=['GET'])
@token_required
def get_post(current_user):
    """"
    This function is use to get all the post
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    all_post=Post.query.all()
    result= posts_schema.dump(all_post)

    return jsonify(result)


@post_blueprint.route('/get/<id>/',methods=['GET'])
@token_required
def post_details(current_user,id):
    """
    This function is use get details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post= Post.query.get(id)
    return post_schema.jsonify(post)


@post_blueprint.route('/update/<id>/',methods=['PUT'])
@token_required
def post_update(current_user,id):
    """
    This function is use to update post details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post=Post.query.get(id)
    data=request.get_json(force=True)

    title=data['title']
    description=data['description']
    
    post.title=title
    post.description=description

    db.session.commit()
    return post_schema.jsonify(post)


@post_blueprint.route('/delete/<id>',methods=['DELETE'])
@token_required
def post_delete(current_user,id):
    """
    This function is use to delete post according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post=Post.query.get(id)
    db.session.delete(post)

    db.session.commit()
    return post_schema.jsonify(post)


