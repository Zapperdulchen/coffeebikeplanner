from datetime import date
from database import init_db, session_db, engine, Event, Location, Plan, Task #, Person
from sample_database import create_sample_db

init_db(engine) # deletes db and recreates it
session = session_db(engine)
create_sample_db(session)

# Get the current date
current_date = date.today()

# Query for all future events
future_events = session.query(Event).filter(Event.start_datetime > current_date).all()

# Example usage: print the names of locations hosting future events
for event in future_events:
    print(f"Event ID: {event.id}, Location: {event.location.name}, Date: {event.start_datetime}, Plan: {event.plans}")

ps = session.query(Plan)
p = ps[0]
