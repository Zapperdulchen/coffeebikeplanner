"""Fügt der Tabelle events die Spalte time_text hinzu.

Die Spalte enthält optional einen Freitext statt der Uhrzeit, z.B.
„nach dem Gottesdienst“. Bestehende Daten bleiben unverändert; ist die Spalte
schon vorhanden, passiert nichts.

Ausführung aus dem Projektverzeichnis:
    python -m housekeeping.add_time_text_column
"""

from sqlalchemy import inspect, text

from database import engine


def add_time_text_column(engine):
    columns = [c['name'] for c in inspect(engine).get_columns('events')]
    if 'time_text' in columns:
        print("Spalte time_text existiert bereits.")
        return
    with engine.begin() as conn:
        conn.execute(text("ALTER TABLE events ADD COLUMN time_text VARCHAR"))
    print("Spalte time_text angelegt.")


if __name__ == '__main__':
    add_time_text_column(engine)
