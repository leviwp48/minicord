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


# ==== initialize db connection ==== 

# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Create the engine
engine = create_engine('sqlite:///minicord.db', echo=True)


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


def get_user(session, username):
    user = session.query(User).filter_by(username=username).first()
    session.commit()
    return user


# this is behind a token check
def update_user(session, user_id, column_name, new_value):
    user = session.query(User).filter_by(id=user_id).first()
    setattr(user, column_name, new_value)
    session.commit()
