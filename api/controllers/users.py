from os import name
from flask import Flask ,request,jsonify,session,make_response,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from api.models.users_models import User
import uuid
from api.models.users_models import db
from api.controllers.login import token_required

user_blueprint = Blueprint('user', __name__,url_prefix='/user')


@user_blueprint.route('/user',methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    This function is to get all user details
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    users=User.query.all()

    output=[]

    for user in users:
        user_data={}
        user_data['public_id']=user.public_id
        user_data['name']=user.name
        user_data['password']=user.password
        user_data['admin']=user.admin
        output.append(user_data)
    return jsonify({'users':output})


@user_blueprint.route('/user/<public_id>',methods=['GET'])
@token_required
def get_one_user(current_user,public_id):
    """
    This function to get user details with their public id number
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'No User Found!'})

    user_data={}
    user_data['public_id']=user.public_id
    user_data['name']=user.name
    user_data['password']=user.password
    user_data['admin']=user.admin
    
    return jsonify({'users':user_data})


@user_blueprint.route('/user',methods=['POST'])
@token_required
def create_user(current_user):
    """
    This function is to create new user in database
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    data=request.get_json(force=True)
    hashed_password = generate_password_hash(data["password"],method="sha256")

    new_user=User(public_id=str(uuid.uuid4()),name=data["name"],password=hashed_password,admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'New User Created!'})


@user_blueprint.route('/user/<public_id>',methods=['PUT'])
@token_required
def promote_user(current_user,public_id):
    """
    This function is to update user details acording to public id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'No User Found!'})

    user.admin=True
    db.session.commit()

    return jsonify({'message':'The User has been promoted!'})


@user_blueprint.route('/user/<public_id>',methods=['DELETE'])
@token_required
def delete_users(current_user,public_id ):
    """
    This function is used to delete the user according to public id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    user=User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message':'No User Found!'})

    db.session.delete(user)
    db.session.commit()    
    return jsonify({'message':'the user has been deleted'})
