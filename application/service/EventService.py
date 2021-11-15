from application.model.Event import Event
from application.model.StudentEvent import StudentEvent
from application.model.Role import Role
from application.service.StudentService import get_id as student_get_id
from application.utilities.database import db
from datetime import *


# Get list of all events
# If created_by is specified, get list of events created by the user
def get_events(created_by=None):
    event_list = []
    if created_by is not None:
        query = db.session.query(Event).filter(
            Event.created_by.in_([created_by]))
        event_list = query.all()
    else:
        query = db.session.query(Event)
        event_list = query.all()

    return event_list


# Get event details of an event
def get_event(event_id):
    event = db.session.query(Event).filter(
        Event._id.in_([event_id])).first()
    return event


def get_upcoming_events(student_email_id):
    student_id = student_get_id(student_email_id)
    student_events = db.session.query(StudentEvent).filter(
        StudentEvent.student_id.in_([student_id]))

    upcoming_events = []

    for student_event in student_events:
        event_id = student_event.event_id
        event = db.session.query(Event).filter(
            Event._id.in_([event_id])).first()
        event_timestamp = event.start_timestamp
        if event_timestamp > datetime.today():
            upcoming_events.append(event)

    return upcoming_events


def register_event(event_id, student_id):
    status = "Registered"
    new_registration = StudentEvent(
        student_id=student_id, event_id=event_id, status=status)

    event = db.session.query(Event).filter_by(
        _id=event_id).first()
    event.registered_count += 1

    db.session.add(new_registration)
    db.session.commit()
    return "Student registered for the event"


def get_registered_events(student_id):
    query = db.session.query(StudentEvent).filter_by(
        student_id=student_id)
    events = query.all()

    return events


# Create new student entry
def create_event(event_information):
    name = event_information['name']
    category = event_information['category']
    description = event_information['description']
    club_id = event_information['club_id']
    visibility = event_information['visibility']
    start_timestamp = event_information['start_timestamp']
    end_timestamp = event_information['end_timestamp']
    location = event_information['location']
    max_registration = event_information['max_registration']
    fee = event_information['fee']
    status = event_information['status']
    registered_count = 0

    new_event = Event(name=name, category=category,
                      description=description, club_id=club_id,
                      visibility=visibility,
                      start_timestamp=start_timestamp,
                      end_timestamp=end_timestamp, location=location,
                      max_registration=max_registration, fee=fee,
                      status=status,
                      registered_count=registered_count)

    db.session.add(new_event)
    db.session.commit()

    return "Event Entry Created"


# Add an event to a club by member/head
def propose_event(event_information, student_id):
    club_id = event_information['club_id']
    role = get_role_in_club(club_id, student_id)
    message = None
    status_code = None

    if role == "Club Member" or role == "Club Head":
        name = event_information['name']
        category = event_information['category']
        description = event_information['description']
        visibility = "Club Member"
        start_timestamp = event_information['start_timestamp']
        end_timestamp = event_information['end_timestamp']
        location = event_information['location']
        max_registration = event_information['max_registration']
        fee = event_information['fee']
        created_by = student_id
        status = "Proposed"
        registered_count = 0

        new_event = Event(name=name, category=category,
                          description=description, club_id=club_id,
                          visibility=visibility,
                          start_timestamp=start_timestamp,
                          end_timestamp=end_timestamp, location=location,
                          max_registration=max_registration, fee=fee,
                          status=status,
                          registered_count=registered_count,
                          created_by=created_by)

        db.session.add(new_event)
        db.session.commit()
        message = "CREATED"
        status_code = 201
    else:
        message = "You do not have the required " \
                  "permissions to perform this operation"
        status_code = 403

    return message, status_code


# Edit an event to a club by member/head
def edit_event(event_information, event_id, student_id):
    club_id = event_information['club_id']
    role = get_role_in_club(club_id, student_id)
    message = None
    status_code = None
    if role == "Club Member" or role == "Club Head":
        event = db.session.query(Event).filter(Event._id.in_(
            [event_id])).update(event_information)
        db.session.commit()
        message = "CREATED"
        status_code = 201
    else:
        message = "You do not have the required" \
                  " permissions to perform this operation"
        status_code = 403

    return message, status_code


# Return the role of student in a club
def get_role_in_club(club_id, student_id):
    query = db.session.query(Role).filter(Role.student_id.in_(
        [student_id]))
    results = query.all()
    role = None

    for result in results:
        if result.club_id == club_id and (
                result.role == "Club Member" or result.role == "Club Head"):
            role = result.role

    return role
