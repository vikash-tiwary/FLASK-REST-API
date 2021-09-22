from os import name
from flask import Flask ,request,jsonify,session,Blueprint
import jwt
import datetime
from api.models.post_models import Address,Author,Post
from api.schema.post_schema import address_schema,addresses_schema
import uuid
from api.controllers.login import token_required
from api.models.users_models import db

address_blueprint = Blueprint('address', __name__,url_prefix='/address')

@address_blueprint.route('/post/<id>',methods=['POST'])
@token_required
def add_address(current_user,id):
    """
    This function is use to create new address in database
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    auth_id=Author.query.get(id)
    data=request.get_json(force=True)

    details=data['details']

    new_address=Address(details=details,author_id=auth_id.id)

    db.session.add(new_address)
    db.session.commit()

    return address_schema.jsonify(new_address)


@address_blueprint.route('/get', methods=['GET'])
@token_required
def get_address(current_user):
    """"
    This function is use to get all the address
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    all_addresses=Address.query.all()
    result= addresses_schema.dump(all_addresses)

    return jsonify(result)


@address_blueprint.route('/get/<id>/',methods=['GET'])
@token_required
def get_address_id(current_user,id):
    """
    This function is use get address details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    address= Address.query.get(id)
    return address_schema.jsonify(address)


@address_blueprint.route('/update/<id>/',methods=['PUT'])
@token_required
def address_update(current_user,id):
    """
    This function is use to update address details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    author=Author.query.get(id)
    data=request.get_json(force=True)

    details=data['details']
    
    author.details=details

    db.session.commit()
    return address_schema.jsonify(author)


@address_blueprint.route('/delete/<id>',methods=['DELETE'])
@token_required
def address_delete(current_user,id):
    """
    This function is use to delete address according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    address=Address.query.get(id)
    db.session.delete(address)

    db.session.commit()
    return address_schema.jsonify(address)
