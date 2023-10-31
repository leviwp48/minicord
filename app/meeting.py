from flask import jsonify
import uuid
import datetime
import orm
import requests
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

def save_meeting(data, meeting_id):
    meeting_id = meeting_id
    host_id = data.get('host_id')
    title = data.get('title')
    participants = data.get('host_id')
    curr_session = orm.open_session()
    res = orm.create_meeting(curr_session, meeting_id, host_id, title, participants)
    orm.close_session(curr_session)
    return res


def join_meeting(data):
    try:
        meeting_id = data.get('meeting_id')
        participant_id = data.get('user_id')
        curr_session = orm.open_session()
        meeting = orm.get_meeting(curr_session, meeting_id)    
        if meeting.id:
            curr_participants = meeting.participants.split(", ")
            for i in curr_participants:
                if i == participant_id:
                    return "User already in meeting"
            formatted_participant = ", " + participant_id
            meeting.participants += formatted_participant
            orm.update_participants(meeting_id, "participants", meeting.participants)
            orm.close_session(curr_session)
            return {'status_code': 200, 'message': 'Successfully joined the meeting.'}
        else:
            orm.close_session(curr_session)
            return {'status_code': 400, 'message': 'Meeting not found.'}
    except Exception as e:
        orm.close_session(curr_session)
        return {'status_code': 500, 'exception': str(e)}


def leave_meeting(data):
    try:
        meeting_id = data.get('meeting_id')
        participant_id = data.get('user_id')
        curr_session = orm.open_session()
        meeting = orm.get_meeting(curr_session, meeting_id)
        if meeting.id:
            curr_participants = meeting.participants.split(", ")
            user_to_remove = None
            for i in curr_participants:
                if i == participant_id:
                    user_to_remove = i
                    break
            if user_to_remove:
                curr_participants.remove(i)
                updated_participants = ', '.join(curr_participants)
                meeting.participants = updated_participants
                orm.update_participants(meeting_id, "participants", meeting.participants)
                orm.close_session(curr_session)
                return {'status_code': 200, 'message': 'Successfully left the meeting.'}
        else:
            orm.close_session(curr_session)
            return {'status_code': 400, 'message': 'Meeting not found.'}
    except Exception as e:
        orm.close_session(curr_session)
        return {'status_code': 500, 'exception': str(e)}
    

def start_twilio_meeting(access_token):


    # Create an Access Token
    token = AccessToken(account_sid, api_key_sid, api_key_secret)

    # Set the Identity of this token
    token.identity = 'user'

    # Grant access to Video
    grant = VideoGrant(room='cool room')
    token.add_grant(grant)

    # Serialize the token as a JWT
    jwt = token.to_jwt().decode('utf-8')

    # Now you can use this jwt in your client-side application
    print(jwt)


    # headers = {
    #     'Authorization': f'Bearer {access_token}',
    #     'Content-Type': 'application/json'
    # }
    # data = {
    #     'topic': 'Example Meeting',
    #     'type': 2
    # }
    # response = requests.post('https://api.zoom.us/v2/users/me/meetings', headers=headers, json=data)
    # print('creating meeting!')
    # if response.status_code == 201:
    #     response_data = response.json()
    #     # Access the 'id' field if it exists
    #     if 'id' in response_data:
    #         meeting_id = response_data['id']
    #         save_meeting(data, meeting_id)
    #     return {'status_code': response.status_code, 'data': response_data, 'message': 'Zoom meeting created successfully!'}
    # else:
    #     return {'status_code': response.status_code, 'message': 'Failed to create meeting'}