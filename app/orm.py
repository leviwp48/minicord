from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, Column, Integer, String, DateTime
from passlib.context import CryptContext
from sqlalchemy.ext.declarative import declarative_base
import datetime


 # ==== models ====


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(60))
    email = Column(String(60), nullable=False)


class Meeting(Base):
    __tablename__ = 'meetings'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    host_id = Column(String(20), unique=True, nullable=False)
    title = Column(String(60))
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    participants = Column(String, nullable=False)


# ==== initialize db connection ==== 

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Create the engine
engine = create_engine('sqlite:///minicord.db', echo=True)
# inspector = inspect(engine)
# if not inspector.has_table('users'):
#     # Create the tables if they do not exist
#     Base.metadata.create_all(engine)
# if not inspector.has_table('meetings'):
#     # Create the tables if they do not exist
#     Base.metadata.create_all(engine)


# ==== sessions ====    

def open_session():
    Session = sessionmaker(bind=engine)
    return Session()

def close_session(session):
    session.close()

# ==== users ==== 

# Add user function
def add_user(session, username, password, email):
    user = User(username=username, password=password, email=email)
    session.add(user)
    session.commit()

# Get user by username and email function
def check_user_exists(session, username, email):
    user = session.query(User).filter_by(username=username, email=email).first()
    session.commit()
    return user


def get_user(session, username, email):
    user = session.query(User).filter_by(username=username, email=email).first()
    session.commit()
    return user


# this is behind a token check
def update_user(session, user_id, column_name, new_value):
    user = session.query(User).filter_by(id=user_id).first()
    setattr(user, column_name, new_value)
    session.commit()


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




