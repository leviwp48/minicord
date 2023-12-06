
'''
    TODO: 
        - add a view for the user logged in 
'''

from flask import Flask, request, jsonify, redirect, session, render_template
from user import user
from meeting import meeting
from decorators import decorators

app = Flask(__name__)
app.debug = True


# Create a route that returns the index.html template
@app.route("/")
def serve_homepage():
    return render_template("index.html")


# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    res = user.register(data)
    return jsonify(res)


# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    res = user.login(data)
    return jsonify(res)


# Persist User Login
@decorators.token_required
@app.route('/keep-login', methods=['POST'])
def keep_login():
    print('here in keep login')
    data = request.get_json()
    res = user.keep_login(data)
    print('returning this: ', res)
    return jsonify(res)


# # User update
# @decorators.token_required
# @app.route('/update-user', methods=['POST'])
# def update_user():
#     data = request.get_json()
#     res = user.update_user(data)
#     return jsonify(res)


# # User update
# @decorators.token_required
# @app.route('/delete-user', methods=['POST'])
# def update_user():
#     data = request.get_json()
#     res = user.delete_user(data)
#     return jsonify(res)


# join a twilio video room
# @decorators.token_required
@app.route("/join-room", methods=["POST"])
def join_room():
    # extract the room_name from the JSON body of the POST request
    room_name = request.json.get("room_name")
    print(room_name)
    # find an existing room with this room_name, or create one
    meeting.find_or_create_room(room_name)
    # retrieve an access token for this room
    access_token = meeting.get_access_token(room_name)
    print(room_name)
    # return the decoded access token in the response
    return {"token": access_token.to_jwt()}


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

