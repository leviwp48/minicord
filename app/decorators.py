from flask import request, jsonify, session, redirect, url_for
import jwt
import os
from functools import wraps

# JWT Token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, os.environ['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated


# decorator to check for the access token in the session
def check_access_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = session.get('access_token')
        if access_token:
            return f(*args, **kwargs)
        else:
            # Redirect to the login page or handle the case when the access token is not available
            return 'no access token'
            # return redirect(url_for('login'))  # Replace 'login' with your login route
    return decorated_function