from datetime import datetime, date
from itertools import repeat, chain
from database import session_db, engine, init_db, create_event, insert_plan, Location, Task, Placeholder, Event, Plan # , Person

def create_sample_db(session):

    # Adding locations
    locations_list = [
        Location(name="Friedhof", external_name="vor dem neuen Friedhof"),
        Location(name="Spielplatz", external_name="auf dem Spielplatz am Hansengarten"),
        Location(name="Hauptstraße", external_name="gegenüber dem Gründlacher Bauernladen"),
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
    tasks = ["Caféradler(in) 1", "Caféradler(in) 2", "Caféradler(in) 3", "Kekslieferant(in)"]
    tasks_list = [Task(task=t) for t in tasks]
    session.add_all(tasks_list)
    session.commit()

    # Adding placeholder texts for tasks
    task4_placeholder = ["Knusperzauberer(in)", "Zuckergusskünstler(in)", "Teigflüsterer(in)"]

    task123_placeholder = ["Plaudertasse", "Schwatzbohne", "Lauschposten",
    "Kekskurier(in)", "Heißgetränkhelfer(in)", "Tortenhörer(in)",
    "Kaffeebotschafter(in)", "Tassentalkmaster(in)"]

    tasks_ids = [session.query(Task).filter(Task.task == t).first() for t in tasks]

    placeholders2tasks_ids = chain(*
                                   [list(zip(ps, repeat(t)))
                                    for ps, t in
                                    zip([task123_placeholder]*3 + [task4_placeholder],
                                        tasks_ids)])

    placeholders_list = [Placeholder(placeholder=p, task_id=t.id)
                         for p, t in placeholders2tasks_ids]
    session.add_all(placeholders_list)
    session.commit()

    # Adding events
    events = [['Spielplatz', '03.05.24 15:00'],
              ['Friedhof', '05.05.24 14:00'],
              ['Hauptstraße', '11.05.24 10:00'],
              ['Spielplatz', '17.05.24 15:00'],
              ['Friedhof', '26.05.24 14:00'],
              ['Hauptstraße', '01.06.24 10:00']]

    for location, start in events:
        create_event(session, location, start)

    # Assigning some person to the necessary tasks for the first event
    # Assuming one person per task for simplicity

    earliest_event = session.query(Event).order_by(Event.start_datetime).first().id
    plans_list = [
        (earliest_event, 'Max Mustermann', tasks_list[0].id),
        # (earliest_event, 'Julia Schneider', tasks_list[1].id),
        # (earliest_event, 'Sophia Becker', tasks_list[2].id),
    ]
    for p in plans_list:
        insert_plan(session, *p)


if __name__ == '__main__':
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
