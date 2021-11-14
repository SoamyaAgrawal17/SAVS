
# def get_events():
#     event_list = ["abc", "def"]
#     return event_list


# def get_event(event_id):
#     event = "abc"
#     return event


# def edit_event(event_id):
#     # update event
#     return "test"

from os import stat
# from app import db
from application.model.Event import Event
from application.model.StudentEvent import StudentEvent
from application.service.StudentService import get_id as student_get_id
from application.utilities.database import db
from datetime import *


def get_events():

    # query = db.session.query(Student).filter(Student.email_id.in_([email_id]))
    # results = query.all()
    # return results

    event_list = ["abcd", "defg"]
    return event_list


def get_event(event_id):
    
    event = db.session.query(Event).filter(Event._id.in_([event_id])).first()
    event_name = event.name
    return event_name

def get_upcoming_events(student_email_id):

    student_id = student_get_id(student_email_id)
    student_events = db.session.query(StudentEvent).filter(StudentEvent.student_id.in_([student_id]))

    upcoming_events = []

    for student_event in student_events:
        event_id = student_event.event_id
        event = db.session.query(Event).filter(Event._id.in_([event_id])).first()
        event_timestamp = event.start_timestamp
        if event_timestamp > datetime.today():
            upcoming_events.append(event)
    
    return upcoming_events



def edit_event(event_id):
    # update event
    return "test"

def register_event(event_id,student_id):

    status = "Registered"
    new_registration = StudentEvent(student_id=student_id, event_id=event_id, status=status)

    event = db.session.query(Event).filter_by(_id=event_id).first()
    event.registered_count += 1

    db.session.add(new_registration)
    db.session.commit()
    return "Student registered for the event"

def get_registered_events(student_id):

    query = db.session.query(StudentEvent).filter_by(student_id=student_id)
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

    new_event = Event(name=name, category=category, description=description, club_id=club_id, visibility=visibility,
                        start_timestamp=start_timestamp, end_timestamp=end_timestamp, location=location,
                        max_registration=max_registration, fee=fee, status=status,
                        registered_count=registered_count)
    
    db.session.add(new_event)
    db.session.commit()

    return "Event Entry Created"

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