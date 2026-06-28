"""Ergänzt die Location „Highland Games“ und den Termin am 01.08.2026.

Das Skript löscht und verändert keine bestehenden Daten. Es legt die Location
und den Termin nur an, falls sie noch nicht vorhanden sind.

Ausführung aus dem Projektverzeichnis:
    python -m housekeeping.add_reutles_event
"""

from datetime import datetime

from database import session_db, engine, create_event, Location, Event


LOCATION_NAME = "Highland Games"
LOCATION_EXTERNAL_NAME = "Highland Games bei St. Felicitas in Reutles"
START_DATETIME = "01.08.26 14:30"
END_DATETIME = "01.08.26 15:30"
DATETIME_FORMAT = "%d.%m.%y %H:%M"


def add_highland_games_event(session):
    """Legt Location und Event an, ohne vorhandene Daten zu verändern."""
    location = session.query(Location).filter_by(name=LOCATION_NAME).first()
    if location is None:
        location = Location(
            name=LOCATION_NAME,
            external_name=LOCATION_EXTERNAL_NAME,
        )
        session.add(location)
        session.commit()
        print(f"Location angelegt: {LOCATION_NAME}")
    else:
        print(f"Location existiert bereits: {LOCATION_NAME}")

    start = datetime.strptime(START_DATETIME, DATETIME_FORMAT)
    event = (
        session.query(Event)
        .filter(
            Event.location_id == location.id,
            Event.start_datetime == start,
        )
        .first()
    )

    if event is None:
        create_event(session, LOCATION_NAME, START_DATETIME, END_DATETIME)
        print("Termin angelegt: 01.08.2026, 14:30–15:30")
    else:
        print("Termin existiert bereits und wurde nicht verändert: "
              "01.08.2026, 14:30")


if __name__ == "__main__":
    session = session_db(engine)
    try:
        add_highland_games_event(session)
    finally:
        session.close()

