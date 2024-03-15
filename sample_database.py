from datetime import datetime
from database import Location, Person, Task, Event, Plan

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
    persons_list = [
        Person(first_name="Max", last_name="Mustermann"),
        Person(first_name="Julia", last_name="Schneider"),
        Person(first_name="Tobias", last_name="Weber"),
        Person(first_name="Sophia", last_name="Becker"),
        Person(first_name="Niklas", last_name="Neumann"),
    ]
    session.add_all(persons_list)
    session.commit()

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
        Event(location_id=locations_list[0].id, date=datetime.strptime("13-3-2024", "%d-%m-%Y")),
        Event(location_id=locations_list[1].id, date=datetime.strptime("15-4-2024", "%d-%m-%Y")),
        Event(location_id=locations_list[2].id, date=datetime.strptime("15-6-2024", "%d-%m-%Y")),
    ]
    session.add_all(events_list)
    session.commit()

    # Assigning some person to the necessary tasks for the first event
    # Assuming one person per task for simplicity
    plans_list = [
        Plan(event_id=events_list[0].id, person_id=persons_list[0].id, task_id=tasks_list[0].id),
        Plan(event_id=events_list[0].id, person_id=persons_list[1].id, task_id=tasks_list[1].id),
        Plan(event_id=events_list[0].id, person_id=persons_list[2].id, task_id=tasks_list[2].id),
    ]
    session.add_all(plans_list)
    session.commit()
