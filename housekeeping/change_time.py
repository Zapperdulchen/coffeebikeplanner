# run using: python -m housekeeping.change_spielplatz_time

# script that sets the start time to 15:00 and the end time to 17:00 for all events at "Spielplatz"

from datetime import datetime, time
from database import session_db, engine, Event, Location

if __name__ == '__main__':
    session = session_db(engine)

    # Find the Location ID for "Spielplatz"
    spielplatz = session.query(Location).filter(Location.name == "Spielplatz").first()

    if not spielplatz:
        print("No location found with name 'Spielplatz'.")
    else:
        events = session.query(Event).filter(Event.location_id == spielplatz.id).all()

        for event in events:
            event_date = event.start_datetime.date()
            event.start_datetime = datetime.combine(event_date, time(15, 0))
            event.end_datetime = datetime.combine(event_date, time(17, 0))

        session.commit()
        print(f"Updated {len(events)} event(s) at 'Spielplatz' to 15:00–17:00.")

