from os import name
from flask import Flask ,request,jsonify,session,make_response,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
import datetime
from api.models.users_models import User
import uuid
from api.models.users_models import app,db

login_blueprint = Blueprint('login', __name__,url_prefix='/login')


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


@login_blueprint.route('/login')
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

