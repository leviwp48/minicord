# old meeting creation code

# Meeting Creation
# @decorators.token_required
# @app.route('/create-meeting', methods=['POST'])
# def create_meeting():
#     print('just got here')
#     data = request.get_json()
#     # Check if the access token is available
#     zoom_access_token = session.get('access_token')
#     # If the access token is not available, redirect to the authorization URL
#     if not zoom_access_token:
#         print('going in here')
#         authorize_url = f'https://zoom.us/oauth/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&data={data}'
#         return redirect(authorize_url)
#     print('doing this')
#     res = meeting.start_zoom_call(zoom_access_token)
#     return jsonify(res)


# @app.route('/join-meeting', methods=['POST'])
# def join_meeting():
#     data = request.get_json()
#     res = meeting.join_meeting(data)
#     return jsonify(res)

# @app.route('/leave-meeting', methods=['POST'])
# def leave_meeting():
#     data = request.get_json()
#     res = meeting.leave_meeting(data)
#     return jsonify(res)




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


    class Meeting(Base):
    __tablename__ = 'meetings'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    host_id = Column(String(20), unique=True, nullable=False)
    title = Column(String(60))
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    participants = Column(String, nullable=False)




# ==== meetings ====
# these are all behind a token check


# id and date_created are automade by the model definitiion
def create_meeting(session, meeting_id, host_id, title, participants):
    try:
        meeting = Meeting(id=meeting_id, host_id=host_id, title=title, participants=participants)
        session.add(meeting)
        session.commit()
        return {'status_code': 200, 'message': 'Meeting successfully created'}
    except Exception as e:
        return {'status_code': 500, 'exception': str(e)}


def get_meeting(session, meeting_id):
    try: 
        meeting = session.query(Meeting).filter_by(id=meeting_id).first()
        session.commit()
        return meeting
    except Exception as e:
        return {'status_code': 500, 'exception': str(e)}


def update_meeting(session, meeting_id, column_name, new_value):
    try:
        meeting = get_meeting(session, meeting_id)
        setattr(meeting, column_name, new_value)
        session.commit()
        return {'status_code': 200, 'message': 'Successfully updated the meeting.'}    
    except Exception as e:
        return {'status_code': 500, 'exception': str(e)}

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
import datetime

engine = create_engine('sqlite:///minicord.db', echo=True)
inspector = inspect(engine)
Base = declarative_base()
if not inspector.has_table('meetings'):
    # Create the tables if they do not exist
    Base.metadata.create_all(engine)



# I don't think this is needed
# class Participant(Base):
#     __tablename__ = 'participants'
#     id = Column(Integer, primary_key=True)
#     meeting_id = Column(Integer, ForeignKey('meetings.id'))
#     user_id = Column(Integer, ForeignKey('users.id'))
#     name = Column(String, nullable=False)
#     join_time = Column(DateTime, default=datetime.now)
#     meeting = relationship("Meeting", back_populates="participants")
#     user = relationship("User", back_populates="participants")