"""Ergänzt die Location „St. Hedwig“ und zwei Termine im Oktober 2026.

Die Termine haben statt einer festen Uhrzeit einen Freitext (time_text). Die
Uhrzeit in START_DATETIME dient nur zur Sortierung.

Das Skript löscht und verändert keine bestehenden Daten. Es legt Location und
Termine nur an, falls sie noch nicht vorhanden sind. Voraussetzung ist die
Spalte time_text (siehe housekeeping/add_time_text_column.py).

Ausführung aus dem Projektverzeichnis:
    python -m housekeeping.add_hedwig_events
"""

from datetime import datetime

from database import session_db, engine, create_event, Location, Event


LOCATION_NAME = "St. Hedwig"
LOCATION_EXTERNAL_NAME = "im Pfarrhof der katholischen Kirche St. Hedwig"
DATETIME_FORMAT = "%d.%m.%y %H:%M"

# (Start, Ende oder None für Start + 2 h, Freitext statt Uhrzeit)
EVENTS = [
    ("04.10.26 10:45", "04.10.26 11:45", "nach dem Erntedankgottesdienst"),
    ("18.10.26 11:00", None, "zum Hedwigsfest [Uhrzeit unklar]"),
]


def add_hedwig_events(session):
    """Legt Location und Events an, ohne vorhandene Daten zu verändern."""
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

    for start_str, end_str, time_text in EVENTS:
        start = datetime.strptime(start_str, DATETIME_FORMAT)
        event = (
            session.query(Event)
            .filter(
                Event.location_id == location.id,
                Event.start_datetime == start,
            )
            .first()
        )
        if event is None:
            create_event(session, LOCATION_NAME, start_str, end_str,
                         time_text=time_text)
            print(f"Termin angelegt: {start:%d.%m.%Y}, {time_text}")
        else:
            when = event.time_text or f"{start:%H:%M}"
            print("Termin existiert bereits und wurde nicht verändert: "
                  f"{start:%d.%m.%Y}, {when}")


if __name__ == "__main__":
    session = session_db(engine)
    try:
        add_hedwig_events(session)
    finally:
        session.close()
