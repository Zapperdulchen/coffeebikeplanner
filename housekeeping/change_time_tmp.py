# run using: python -m housekeeping.change_time_tmp

# script that sets the start time to 14:30 and the end time to 16:30
# for all events at "Highland Games"

from datetime import datetime, time
from database import session_db, engine, Event, Location

LOCATION_NAME = "Highland Games"

if __name__ == '__main__':
    session = session_db(engine)

    # Find the Location ID for the configured location
    location = session.query(Location).filter(
        Location.name == LOCATION_NAME
    ).first()

    if not location:
        print(f"No location found with name '{LOCATION_NAME}'.")
    else:
        events = session.query(Event).filter(
            Event.location_id == location.id
        ).all()

        for event in events:
            event_date = event.start_datetime.date()
            event.start_datetime = datetime.combine(event_date, time(14, 30))
            event.end_datetime = datetime.combine(event_date, time(16, 30))

        session.commit()
        print(
            f"Updated {len(events)} event(s) at '{LOCATION_NAME}' "
            "to 14:30–16:30."
        )
