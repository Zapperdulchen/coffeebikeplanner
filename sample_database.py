from datetime import datetime
from database import insert_plan, Location, Task, Event, Plan # , Person

def create_sample_db(session):

    # Adding locations
    locations_list = [
        Location(name="Friedhof", address="Address 1"),
        Location(name="Spielplatz", address="Address 2"),
        Location(name="Hauptstraße", address="Address 3"),
    ]
    session.add_all(locations_list)
    session.commit()

    # Creating 5 dummy persons
    # persons_list = [
    #     Person(first_name="Max", last_name="Mustermann"),
    #     Person(first_name="Julia", last_name="Schneider"),
    #     Person(first_name="Tobias", last_name="Weber"),
    #     Person(first_name="Sophia", last_name="Becker"),
    #     Person(first_name="Niklas", last_name="Neumann"),
    # ]
    # session.add_all(persons_list)
    # session.commit()

    # Adding tasks
    tasks_list = [
        Task(task="Plaudertasse"),
        Task(task="Schwatzbohne"),
        Task(task="Lauschbecher"),
        Task(task="Knusperzauberer"),
    ]
    session.add_all(tasks_list)
    session.commit()

    # Adding events
    events_list = [
        Event(location_id=locations_list[0].id, start_datetime=datetime.strptime("14.04.24 14:00", '%d.%m.%y %H:%M'), end_datetime=datetime.strptime("14.04.24 16:00", '%d.%m.%y %H:%M')),
        Event(location_id=locations_list[1].id, start_datetime=datetime.strptime("17.04.24 10:00", '%d.%m.%y %H:%M'), end_datetime=datetime.strptime("17.04.24 12:00", '%d.%m.%y %H:%M')),
        Event(location_id=locations_list[2].id, start_datetime=datetime.strptime("19.04.24 14:00", '%d.%m.%y %H:%M'), end_datetime=datetime.strptime("19.04.24 16:00", '%d.%m.%y %H:%M')),
    ]
    session.add_all(events_list)
    session.commit()

    # Assigning some person to the necessary tasks for the first event
    # Assuming one person per task for simplicity
    plans_list = [
        (events_list[0].id, 'Max Mustermann', tasks_list[0].id),
        (events_list[0].id, 'Julia Schneider', tasks_list[1].id),
        (events_list[0].id, 'Sophia Becker', tasks_list[2].id),
    ]
    for p in plans_list:
        insert_plan(session, *p)
