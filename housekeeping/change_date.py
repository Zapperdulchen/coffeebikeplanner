# run using python -m housekeeping.change_date

from datetime import datetime, date
from database import session_db, engine, init_db, create_event, insert_plan, Location, Task, Placeholder, Event, Plan # , Person

if __name__ == '__main__':
    session = session_db(engine)

    e = session.query(Event).filter(Event.start_datetime < date(2024,5,4)).all()[0]
    e.start_datetime = datetime(2024,5,2,15,0)
    e.end_datetime = datetime(2024,5,2,17,0)
    session.commit()

