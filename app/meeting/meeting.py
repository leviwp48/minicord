import uuid
import twilio.jwt.access_token
import twilio.jwt.access_token.grants
import twilio.rest
import os 


account_sid = os.getenv('ACCOUNT_SID')
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
twilio_client = twilio.rest.Client(api_key, api_secret, account_sid)


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
