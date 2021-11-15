
from application.model.Student import Student
from application.model.Event import Event
from application.model.StudentEvent import StudentEvent
from application.model.Role import Role
from application.model.Club import Club
from application.service.ClubService import get_id as get_club_id
from application.service.ClubService import club_exist
from application.utilities.database import db
from datetime import *


def get_id(email_id):
    student = db.session.query(Student).filter(Student.email_id.in_([email_id])).first()
    if student is None:
        return None
    student_id = student._id
    return student_id


def check_if_already_registered(event_id, student_id):
    query = db.session.query(StudentEvent).filter_by(student_id=student_id, event_id=event_id)
    result = query.all()
    return len(result) > 0


# Signup a student
def create_student(student_information):
    name = student_information['name']
    email_id = student_information['email_id']
    college = student_information['college']
    department = student_information['department']

    new_student = Student(name=name, email_id=email_id, college=college,
                          department=department)
    db.session.add(new_student)
    db.session.commit()
    return "Student Entry Created"


# Get student information
def get_student(email_id=None):
    query = db.session.query(Student).filter(Student.email_id.in_([email_id]))
    result = query.first()
    return result.as_dict()


# View all upcoming events.
def get_upcoming_events(student_email_id):
    student_id = get_id(student_email_id)
    student_events = db.session.query(StudentEvent).filter(StudentEvent.student_id.in_([student_id]))

    upcoming_events = []

    for student_event in student_events:
        event_id = student_event.event_id
        event = db.session.query(Event).filter(Event._id.in_([event_id])).first()
        event_timestamp = event.start_timestamp
        if event_timestamp > datetime.today():
            upcoming_events.append(event.as_dict())

    return upcoming_events


# Register for an event
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


# View registered events
def get_registered_events(student_id):

    query = db.session.query(StudentEvent).filter_by(student_id=student_id)
    events = query.all()
    registered_events = []
    for event in events:
        registered_events.append(event.as_dict())
    return registered_events


# Create a new club
def create_club(club_information):
    name = club_information['name']
    head = club_information['head']
    category = club_information['category']
    description = club_information['description']

    if club_exist(name):
        return 201, "Club with same name already exist"

    new_club = Club(name=name, head=head, category=category, description=description)

    db.session.add(new_club)
    db.session.commit()

    student_id = get_id(head)
    club_id = get_club_id(name)
    role = "Club Head"

    new_role = Role(student_id=student_id, club_id=club_id, role=role)
    db.session.add(new_role)
    db.session.commit()

    return 200, "Club Entry Created"


def get_roles(student_id):
    query = db.session.query(Role).filter_by(student_id=student_id)
    clubs_response = query.all()
    clubs = []
    for club in clubs_response:
        clubs.append(club.as_dict())
    return clubs

# {
#     "name": "TestStudent",
#     "email_id": "test_student@columbia.edu",
#     "college": "Fu Foundation",
#     "department": "Computer Science"
# }
