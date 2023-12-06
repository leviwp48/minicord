from flask import jsonify, session
import os
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from orm import orm

def register(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    curr_session = orm.open_session()
    # Check if the username already exists
    user = orm.check_user_exists(curr_session, username, email)
    if user:
        orm.close_session(curr_session)
        return {'status_code': 400, 'message': 'Username and email already exists. Please choose a different username or email.'}
    # Hash the password before storing it (using Werkzeug's generate_password_hash)
    hashed_password = generate_password_hash(password, method='sha256')
    orm.add_user(curr_session, username, hashed_password, email)
    orm.close_session(curr_session)
    return {'status_code': 200, 'message': 'User successfully created'}


def login(data):
    username = data.get('username')
    password = data.get('password')
    curr_session = orm.open_session()
    # Check if the user exists and the password is correct
    user = orm.get_user(curr_session, username)
    passwords_match = check_password_hash(user.password, password)
    orm.close_session(curr_session)
    if passwords_match:
        print('here')
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.environ.get('SECRET_KEY'))
        res = {'status_code': 200, 'message': 'successfully logged in', 'token': token}
        print(res['token'])
        return res
    else:
        return {'status_code': 401, 'message': 'Invalid username or password'}
    

def keep_login(data):
    user_token = data.get('storedToken')
    if user_token:
        try:
            # Decode the token
            decoded_token = jwt.decode(user_token, os.environ['SECRET_KEY'], algorithms=["HS256"])
            username = decoded_token.get('user', 'unknown')
            res = {'status_code': 200, 'message': 'successfully logged in', 'username': username}
            print(res)
        except jwt.ExpiredSignatureError:
            res = {'status_code': 400, 'message': 'Token has expired'}
        except jwt.InvalidTokenError:
            res = {'status_code': 400, 'message': 'Invalid token'}
    else:
        res = {'status_code': 401, 'message': 'No token saved'}
   
    print(res)
    return res
    

def update_user(data):
    username = data.get('username')
    email = data.get('email')
    column_name = data.get('column_name')
    value = data.get('value')
    curr_session = orm.open_session()
    user = orm.get_user(curr_session, username, email)
    if user:
        orm.update_user(curr_session, user.id, column_name, value)
    orm.close_session(curr_session)
