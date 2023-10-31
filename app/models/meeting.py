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