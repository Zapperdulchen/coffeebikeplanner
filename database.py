from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

sqlite_db = 'sqlite:///plan.db'
engine = create_engine(sqlite_db)

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    location = relationship("Location", back_populates="events")

Location.events = relationship("Event", order_by=Event.id, back_populates="location")

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    task = Column(String)

# class Person(Base):
#     __tablename__ = 'persons'
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String)
#     last_name = Column(String)

class Plan(Base):
    __tablename__ = 'plans'
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    # person_id = Column(Integer, ForeignKey('persons.id'))
    person = Column(String)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    event = relationship("Event", back_populates="plans")
    # person = relationship("Person", back_populates="plans")
    task = relationship("Task")

Event.plans = relationship("Plan", back_populates="event")
# Person.plans = relationship("Plan", back_populates="person")


class PlanAuditLog(Base):
    __tablename__ = 'plan_audit_log'
    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey('plans.id'))
    changed_at = Column(DateTime, default=datetime.utcnow)
    operation = Column(String)  # 'ADD' or 'UPDATE'
    previous_state = Column(String)  # JSON or similar serialization


class Placeholder(Base):
    __tablename__ = 'placeholder'
    id = Column(Integer, primary_key=True)
    placeholder = Column(String)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    task = relationship("Task")

Task.placeholders = relationship("Placeholder", back_populates="task")



def init_db(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def session_db(engine):
    Session = sessionmaker(bind=engine)
    return Session()


def create_event(session, location_name, start_datetime_str, end_datetime_str=None):
    """
    Creates a new event based on the location name and start datetime.
    If end datetime is not provided, adds 2 hours to the start datetime.

    Args:
    - session: SQLAlchemy Session object to interact with the database.
    - location_name: The name of the location where the event will take place.
    - start_datetime_str: The start datetime of the event in 'YYYY-MM-DD HH:MM' format.
    - end_datetime_str: Optional; The end datetime of the event in 'YYYY-MM-DD HH:MM' format.

    Returns:
    The ID of the new event or None in case of error.
    """
    start_datetime = datetime.strptime(start_datetime_str, "%d.%m.%y %H:%M")
    if end_datetime_str:
        end_datetime = datetime.strptime(end_datetime_str, "%d.%m.%y %H:%M")
    else:
        end_datetime = start_datetime + timedelta(hours=2)  # Add 2 hours if end datetime is not provided

    # Find the location by name
    location = session.query(Location).filter_by(name=location_name).first()

    if location is None:
        print(f"Location with name '{location_name}' not found.") # DBG
        return None

    # Create a new Event object
    new_event = Event(location_id=location.id, start_datetime=start_datetime, end_datetime=end_datetime)

    # Add the new event to the session and commit
    session.add(new_event)
    session.commit()

    return new_event.id


def insert_plan(session, event_id, person, task_id):
    """
    Inserts or updates a plan for a given event and task, associating it with a
    specific person.

    This function first attempts to find an existing plan that matches the
    given event_id and task_id. If such a plan is found, it proceeds to update
    this plan by associating it with the given person. If no existing plan is
    found, a new plan is created and added to the database with the specified
    event_id, task_id, and person.

    Additionally an audit log entry is made to record the operation. The audit
    log includes the operation type (ADD for new plans or UPDATE for existing
    ones), the previous state of the plan, and the identifiers involved
    (event_id and task_id).

    Parameters:
    - session: The SQLAlchemy session used to interact with the database.
    - event_id: The ID of the event associated with the plan.
    - person: The person to be associated with the plan. This can be a model
      instance or an identifier, depending on implementation.
    - task_id: The ID of the task associated with the plan.

    Returns:
    The ID of the plan that was added or updated or None in case of error.
    """
    print('insert_plan: ', event_id, person, task_id) # DBG
    # Try to find an existing plan with the given event_id and task_id
    plan = session.query(Plan).filter_by(event_id=event_id, task_id=task_id).first()

    operation = 'UPDATE' if plan and plan.person != person else None

    # If no existing plan is found, create a new one
    if not plan:
        plan = Plan(event_id=event_id, task_id=task_id)
        session.add(plan)
        operation = 'ADD'

    if operation:
        # Create an audit log for the modification
        session.add(PlanAuditLog(plan_id=plan.id,
                                operation=operation,
                                previous_state=";".join([str(event_id),
                                                        str(task_id),
                                                        (plan.person
                                                        if plan.person else 'NONE')])))
        plan.person = person
        session.commit()

        return plan.id
    else:
        return None


def delete_plan(session, event_id, task_id):
    """
    Deletes a specific plan identified by an event_id and a task_id from the
    database.

    This function searches for a plan matching the provided event_id and
    task_id. If such a plan is found, it is deleted from the database. Before
    deletion, an audit log entry is created to record the deletion operation,
    including the state of the plan before its removal. This audit log captures
    the event_id, task_id, and associated person (if any) as part of the plan's
    previous state.

    Parameters:
    - session: The SQLAlchemy session used to interact with the database.
    - event_id: The ID of the event associated with the plan to be deleted.
    - task_id: The ID of the task associated with the plan to be deleted.

    Returns:
    The ID of the deleted plan or None in case of error resp. if no plan was
    found
    """
    print('delete_plan: ', event_id, task_id) # DBG
    # Try to find an existing plan with the given event_id and task_id
    plan = session.query(Plan).filter_by(event_id=event_id, task_id=task_id).first()

    if plan:
        # Create an audit log for the modification
        session.add(PlanAuditLog(plan_id=plan.id,
                                operation='DELETE',
                                previous_state=";".join([str(event_id),
                                                        str(task_id),
                                                        (plan.person
                                                        if plan.person else 'NONE')])))
        session.delete(plan)
        session.commit()

        return plan.id
    else:
        return None
