from os import name
from flask import Flask ,request,jsonify,session,make_response,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from api.models import app,db,Address,Author,Post
from api.schemas import PostSchema,post_schema,posts_schema,auths_schema,auth_schema,address_schema,addresses_schema
from api.models import User
import uuid

user_blueprint = Blueprint('user', __name__,url_prefix='/user')
post_blueprint = Blueprint('post', __name__,url_prefix='/post')



def token_required(f):
    """
    This is a decorator function for token authenticatio
    """
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None

        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']

        if not token:
            return jsonify({'message':'Token is missing!'}),401

        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            current_user=User.query.filter_by(public_id=data['public_id']).first()

        except:
            return jsonify({'message':'Token is invalid'}),401

        return f(current_user,*args,**kwargs)

    return decorated





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





@user_blueprint.route('/login')
def login():
    """
    This function is use to create authentiacation token
    """
    auth=request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})
    
    user=User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})

    if check_password_hash(user.password,auth.password):
        token=jwt.encode({'public_id':user.public_id,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])

        return jsonify({'token':token.decode()})
        #return jsonify({'token':token})

    return make_response('Could not verify',401,{'WWW-Authenticate':'Basic realm="Login required!"'})






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





@post_blueprint.route('/post_details/<id>/',methods=['GET'])
@token_required
def post_details(current_user,id):
    """
    This function is use get details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post= Post.query.get(id)
    return post_schema.jsonify(post)






@post_blueprint.route('/post_update/<id>/',methods=['PUT'])
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





@post_blueprint.route('/author/<id>',methods=['POST'])
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





@post_blueprint.route('/get_author', methods=['GET'])
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





@post_blueprint.route('/get_author/<id>/',methods=['GET'])
@token_required
def get_author_id(current_user,id):
    """
    This function is use get author details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    author= Author.query.get(id)
    return auth_schema.jsonify(author)




@post_blueprint.route('/author_update/<id>/',methods=['PUT'])
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





@post_blueprint.route('/author_delete/<id>',methods=['DELETE'])
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




@post_blueprint.route('/address/<id>',methods=['POST'])
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




@post_blueprint.route('/get_address', methods=['GET'])
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




@post_blueprint.route('/get_address/<id>/',methods=['GET'])
@token_required
def get_address_id(current_user,id):
    """
    This function is use get address details according to id
    """
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    address= Address.query.get(id)
    return address_schema.jsonify(address)




@post_blueprint.route('/address_delete/<id>',methods=['DELETE'])
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
