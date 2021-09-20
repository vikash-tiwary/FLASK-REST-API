from flask import Flask ,request,jsonify,session,make_response,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from .models import app
from .models import User


user_blueprint = Blueprint('user', __name__,url_prefix='/user')
post_blueprint = Blueprint('post', __name__,url_prefix='/post')


def token_required(f):
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
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    data=request.get_json()
    hashed_password = generate_password_hash(data["password"],method="sha256")

    new_user=User(public_id=str(uuid.uuid4()),name=data["name"],password=hashed_password,admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message':'New User Created!'})

@user_blueprint.route('/user/<public_id>',methods=['PUT'])
@token_required
def promote_user(public_id):
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
def delete_users(public_id ):
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
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})

    title=request.json['title']
    description=request.json['description']
    author=request.json['author']

    my_posts=Post(title,description,author)
    db.session.add(my_posts)
    db.session.commit()

    return post_schema.jsonify(my_posts)



@post_blueprint.route('/get', methods=['GET'])
@token_required
def get_post(current_user):
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    all_post=Post.query.all()
    result= posts_schema.dump(all_post)

    return jsonify(result)


@post_blueprint.route('/post_details/<id>/',methods=['GET'])
@token_required
def post_details(current_user,id):
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post= Post.query.get(id)
    return post_schema.jsonify(post)


@post_blueprint.route('/post_update/<id>/',methods=['PUT'])
@token_required
def post_update(current_user,id):
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post=Post.query.get(id)

    title=request.json['title']
    description=request.json['description']
    author=request.json['author']


    post.title=title
    post.description=description
    post.author=author

    db.session.commit()
    return post_schema.jsonify(post)


@post_blueprint.route('/delete/<id>',methods=['DELETE'])
@token_required
def post_delete(current_user,id):
    if not current_user.admin:
        return jsonify({'message':'Cannot perform that function'})
    post=Post.query.get(id)
    db.session.delete(post)

    db.session.commit()
    return post_schema.jsonify(post)

