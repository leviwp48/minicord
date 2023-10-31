from flask import jsonify
import os
import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import orm

def register(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    curr_session = orm.open_session()
    # Check if the username already exists
    user = orm.check_user_exists(curr_session, username, email)
    if user:
        orm.close_session(curr_session)
        return {'status_code': 400, 'message': 'Username or email already exists. Please choose a different username or email.'}
    # Hash the password before storing it (using Werkzeug's generate_password_hash)
    hashed_password = generate_password_hash(password, method='sha256')
    orm.add_user(curr_session, username, hashed_password, email)
    orm.close_session(curr_session)
    return {'status_code': 200, 'message': 'User successfully created'}


def login(data):
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    curr_session = orm.open_session()
    # Check if the user exists and the password is correct
    user = orm.get_user(curr_session, username, email)
    passwords_match = check_password_hash(user.password, password)
    orm.close_session(curr_session)
    if passwords_match:
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, os.environ.get('SECRET_KEY'))
        return {'token': token}
    else:
        return {'status_code': 401, 'message': 'Invalid username or password'}

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
