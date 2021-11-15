from os import stat
from application.model.Event import Event
from application.model.Role import Role
from application.model.StudentEvent import StudentEvent
from application.service.StudentService import get_id as student_get_id
from application.utilities.database import db
from datetime import *


def get_role_in_club(club_id, student_id):
    query = db.session.query(Role).filter(Role.student_id.in_([student_id]))
    results = query.all()
    role = None

    for result in results:
        if result.club_id == club_id and (result.role == "Club Member" or result.role == "Club Head"):
            role = result.role

    return role


def get_events(created_by=None):
    event_list = []
    if created_by is not None:
        query = db.session.query(Event).filter(Event.created_by.in_([created_by]))
        event_list = query.all()
    else:
        query = db.session.query(Event)
        event_list = query.all()

    events = [event.as_dict() for event in event_list]
    return events


def get_upcoming_events(student_email_id):
    student_id = student_get_id(student_email_id)
    student_events = db.session.query(StudentEvent).filter(StudentEvent.student_id.in_([student_id]))

    upcoming_events = []

    for student_event in student_events:
        event_id = student_event.event_id
        event = db.session.query(Event).filter(Event._id.in_([event_id])).first()
        event_timestamp = event.start_timestamp
        if event_timestamp > datetime.today():
            upcoming_events.append(event.as_dict())
    
    return upcoming_events


def get_event_details(event_id):
    query = db.session.query(Event).filter_by(_id=event_id)
    return query.first().as_dict()


def check_if_already_registered(event_id, student_id):
    query = db.session.query(StudentEvent).filter_by(student_id=student_id, event_id=event_id)
    result = query.all()
    return len(result) > 0


def register_event(event_id, student_id):
    status = "Registered"
    if check_if_already_registered(event_id, student_id):
        return "Student already registered for the event"
    new_registration = StudentEvent(student_id=student_id, event_id=event_id, status=status)

    event = db.session.query(Event).filter_by(_id=event_id).first()
    event.registered_count += 1

    db.session.add(new_registration)
    db.session.commit()
    return "Student registered for the event"


def get_registered_events(student_id):

    query = db.session.query(StudentEvent).filter_by(student_id=student_id)
    events = query.all()
    registered_events = []
    for event in events:
        registered_events.append(event.as_dict())
    return registered_events


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

        new_event = Event(name=name, category=category, description=description, club_id=club_id, visibility=visibility,
                          start_timestamp=start_timestamp, end_timestamp=end_timestamp, location=location,
                          max_registration=max_registration, fee=fee, status=status,
                          registered_count=registered_count, created_by=created_by)

        db.session.add(new_event)
        db.session.commit()
        message = "CREATED"
        status_code = 201
    else:
        message = "You do not have the required permissions to perform this operation"
        status_code = 403

    return message, status_code

# {
#   "name": "Test Event",
#   "category": "Test Event Category",
#   "description": "Test Event Description",
#   "club_id": 1,
#   "visibility": "all",
#   "start_timestamp": "2021-12-23T18:00:00.000Z",
#   "end_timestamp": "2021-12-25T18:00:00.000Z",
#   "location": "Test Event Location",
#   "max_registration": 100,
#   "fee": 10,
#   "status": "Approved"
# }