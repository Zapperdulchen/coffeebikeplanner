from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

sqlite_db = 'sqlite:///plan.db'
engine = create_engine(sqlite_db)

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    date = Column(Date)
    location = relationship("Location", back_populates="events")

Location.events = relationship("Event", order_by=Event.id, back_populates="location")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task = Column(String)

class Person(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    person_id = Column(Integer, ForeignKey('persons.id'))
    task_id = Column(Integer, ForeignKey('tasks.id'))
    event = relationship("Event", back_populates="plans")
    person = relationship("Person", back_populates="plans")
    task = relationship("Task")

Event.plans = relationship("Plan", back_populates="event")
Person.plans = relationship("Plan", back_populates="person")

def init_db(engine):
    Base.metadata.create_all(engine)

def session_db(engine):
    Session = sessionmaker(bind=engine)
    return Session()

# new_location = Location(name="Example Location", address="123 Example St")
# session.add(new_location)
# session.commit()

# event = session.query(Event).filter_by(date='2024-03-13').first()
# print(event)

# from datetime import date
# from sqlalchemy.orm import Session

# # Assuming you have already created the engine and session as shown previously
# session = Session(bind=engine)

# # Get the current date
# current_date = date.today()

# # Query for all future events
# future_events = session.query(Event).filter(Event.date > current_date).all()

# # Example usage: print the names of locations hosting future events
# for event in future_events:
#     print(f"Event ID: {event.id}, Location: {event.location.name}, Date: {event.date}")

