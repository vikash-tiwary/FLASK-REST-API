from os import name
from flask import Flask ,request,jsonify,session,Blueprint
import jwt
import datetime
from api.models.post_models import Address,Author,Post
from api.schema.post_schema import auths_schema,auth_schema
import uuid
from api.controllers.login import token_required
from api.models.users_models import db

author_blueprint = Blueprint('author', __name__,url_prefix='/author')

@author_blueprint.route('/post/<id>',methods=['POST'])
@token_required
def add_author(current_user,id):
    """
    This function is use to create new author in database
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    post_id=Post.query.get(id)
    data=request.get_json(force=True)

    name=data['name']

    new_author=Author(name=name,post_id=post_id.id)

    db.session.add(new_author)
    db.session.commit()

    return auth_schema.jsonify(new_author)


@author_blueprint.route('/get', methods=['GET'])
@token_required
def get_author(current_user):
    """"
    This function is use to get all the author
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    all_author=Author.query.all()
    result= auths_schema.dump(all_author)

    return jsonify(result)


@author_blueprint.route('/get/<id>/',methods=['GET'])
@token_required
def get_author_id(current_user,id):
    """
    This function is use get author details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    author= Author.query.get(id)
    return auth_schema.jsonify(author)


@author_blueprint.route('/update/<id>/',methods=['PUT'])
@token_required
def author_update(current_user,id):
    """
    This function is use to update author details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    author=Author.query.get(id)
    data=request.get_json(force=True)

    name=data['name']
    
    author.name=name

    db.session.commit()
    return auth_schema.jsonify(author)


@author_blueprint.route('/delete/<id>',methods=['DELETE'])
@token_required
def author_delete(current_user,id):
    """
    This function is use to delete post according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    author=Author.query.get(id)
    db.session.delete(author)

    db.session.commit()
    return auth_schema.jsonify(author)

