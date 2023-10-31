from flask import Flask, request, jsonify, redirect, session, render_template
import auth.auth as auth 
import auth.oauth as oauth
import meeting
import decorators
import requests
import twilio.jwt.access_token
import twilio.jwt.access_token.grants
import twilio.rest
import uuid
import os

# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'AC31b8b1202a342fc06d6ecac6f1012f5c'
api_key = 'SK482a8451d95a4a640851c9cc63f09a22'
api_secret = '7ibXcPSY0Lek5ONdpmecHXcfnjzAKbNh'
twilio_client = twilio.rest.Client(api_key, api_secret, account_sid)

app = Flask(__name__)
app.debug = True

def find_or_create_room(room_name):
    try:
        # try to fetch an in-progress room with this name
        twilio_client.video.rooms(room_name).fetch()
    except twilio.base.exceptions.TwilioRestException:
        # the room did not exist, so create it
        twilio_client.video.rooms.create(unique_name=room_name, type="go")

def get_access_token(room_name):
    # create the access token
    access_token = twilio.jwt.access_token.AccessToken(
        account_sid, api_key, api_secret, identity=uuid.uuid4().int
    )
    # create the video grant
    video_grant = twilio.jwt.access_token.grants.VideoGrant(room=room_name)
    # Add the video grant to the access token
    access_token.add_grant(video_grant)
    return access_token

# @app.route('/', methods=['GET'])
# def test():
#     res = {'message': 'something!'}
#     return jsonify(res)

# Create a route that returns the index.html template
@app.route("/")
def serve_homepage():
    return render_template("index.html")

@app.route("/join-room", methods=["POST"])
def join_room():
    # extract the room_name from the JSON body of the POST request
    room_name = request.json.get("room_name")
    # find an existing room with this room_name, or create one
    find_or_create_room(room_name)
    # retrieve an access token for this room
    access_token = get_access_token(room_name)
    # return the decoded access token in the response
    # NOTE: if you are using version 6 of the Python Twilio Helper Library,
    # you should call `access_token.to_jwt().decode()`
    return {"token": access_token.to_jwt()}

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    res = auth.register(data)
    return jsonify(res)

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    res = auth.login(data)
    return jsonify(res)

# User update
@decorators.token_required
@app.route('/update-user', methods=['POST'])
def update_user():
    data = request.get_json()
    res = auth.update_user(data)
    return jsonify(res)


# Meeting Creation
# @decorators.token_required
@app.route('/create-meeting', methods=['POST'])
def create_meeting():
    print('just got here')
    data = request.get_json()
    # Check if the access token is available
    zoom_access_token = session.get('access_token')
    # If the access token is not available, redirect to the authorization URL
    if not zoom_access_token:
        print('going in here')
        authorize_url = f'https://zoom.us/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&data={data}'
        return redirect(authorize_url)
    print('doing this')
    res = meeting.start_zoom_call(zoom_access_token)
    return jsonify(res)


@app.route('/join-meeting', methods=['POST'])
def join_meeting():
    data = request.get_json()
    res = meeting.join_meeting(data)
    return jsonify(res)

@app.route('/leave-meeting', methods=['POST'])
def leave_meeting():
    data = request.get_json()
    res = meeting.leave_meeting(data)
    return jsonify(res)


# ==== zoom api ====

# Step 2: Handle the callback from Zoom's OAuth
# @app.route('/oauth/callback')
# def zoom_oauth_callback():
#     code = request.args.get('code')
#     # data = request.args.get('data')
#     oauth.oauth_callback(code, REDIRECT_URI)
#     create_meeting_url = "http://localhost/create-meeting"  # Modify the URL according to your setup
#     print('about to redirect')
#     headers = {
#         'Content-Type': 'application/json'
#     }
#     data = {"host_id": "levi", "title": "levi meeting" }
#     res = requests.post(create_meeting_url, headers=headers, json=data)
#     print(res.status_code)
#     what =  {'message': 'something!'}
#     return jsonify(what)
#     # return jsonify({'message': 'done'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

