from application.model.Student import Student
from application.model.Event import Event
from application.model.StudentEvent import StudentEvent
from application.model.Role import Role
from application.model.Club import Club
from application.service.ClubService import get_id as get_club_id
from application.service.ClubService import club_exist
from application.service.EventService import get_event
from application.utilities.database import db
from datetime import datetime


# Variable declaration
student_does_not_exist = "Student does not exist"


# Get student id if email_id of student is provided
def get_id(email_id):
    student = db.session.query(Student).filter(
        Student.email_id.in_([email_id])).first()
    if student is None:
        return student_does_not_exist
    student_id = student._id
    return student_id


# Check if a student is already registered for
# a particular event
def check_if_already_registered(event_id, student_id):
    query = db.session.query(StudentEvent).filter_by(
        student_id=student_id, event_id=event_id)
    result = query.all()
    return len(result) > 0


# Signup a student
def create_student(student_information):
    if ('name' not in student_information or
            'email_id' not in student_information or
            'college' not in student_information or
            'department' not in student_information):
        return ("Missing information(name, email_id, college, " +
                "department) required to create student")
    name = student_information['name']
    email_id = student_information['email_id']
    college = student_information['college']
    department = student_information['department']

    if get_student(email_id) != student_does_not_exist:
        return "Student Already Exists"

    new_student = Student(name=name, email_id=email_id, college=college,
                          department=department)
    db.session.add(new_student)
    db.session.commit()
    return "Student Entry Created"


# Get student information
def get_student(email_id=None):
    query = db.session.query(Student).filter(Student.email_id.in_([email_id]))
    result = query.first()
    if result is None:
        return student_does_not_exist
    return result.as_dict()


# View all upcoming events.
def get_upcoming_events(student_id):
    student_events = db.session.query(StudentEvent).filter(
        StudentEvent.student_id.in_([student_id])).all()
    student_events.sort(key=lambda x: x.event_id)
    upcoming_events = []

    for student_event in student_events:
        event_id = student_event.event_id
        event = db.session.query(Event).filter(Event._id.in_(
            [event_id])).first()
        event_timestamp = event.start_timestamp
        if event_timestamp > datetime.today():
            upcoming_events.append(event.as_dict())

    return upcoming_events


# Register for an event
def register_event(event_id, student_id):
    status = "Registered"
    if check_if_already_registered(event_id, student_id):
        return "Student already registered for the event"

    # Check if student is eligible to register based on club
    event = get_event(event_id)

    if event.get_time_status_() == "Past":
        return "You cannot register for an event in the past"

    if event.visibility == "Club Member":
        query = db.session.query(Role).\
                filter_by(student_id=student_id, club_id=event.club_id)
        clubs_response = query.all()
        if len(clubs_response) == 0:
            return ("You need to be part of " +
                    "this club to register for this event.")

    if event.registered_count == event.max_registration:
        return "The event is at maximum capacity"

    # Register for event
    new_registration = StudentEvent(student_id=student_id,
                                    event_id=event_id, status=status)

    event = db.session.query(Event).filter_by(_id=event_id).first()
    event.registered_count += 1
    db.session.add(new_registration)
    db.session.commit()
    return "Student registered for the event"


# View registered events
def get_registered_events(student_id):
    query = db.session.query(StudentEvent).filter_by(student_id=student_id)
    student_events = query.all()
    student_events.sort(key=lambda x: x.event_id)
    registered_events = []
    for student_event_id in student_events:
        event = db.session.query(Event).\
                filter_by(_id=student_event_id.event_id).first()
        json_response = {
            "student_id": student_id,
            "event": event.as_dict(),
            "status": student_event_id.status
        }
        registered_events.append(json_response)

    return registered_events


# Withdraw event
def withdraw_event(student_id, event_id):
    query = db.session.query(StudentEvent).\
            filter_by(student_id=student_id, event_id=event_id)
    student_event = query.first()
    if student_event is None:
        return "Failure: Can't withdraw from an event not registered in"
    event_id = student_event.event_id
    event = db.session.query(Event).filter_by(_id=event_id).first()

    if event.get_time_status_() == "Past":
        return "Failure: Can't withdraw from past event"
    student_event.status = "Withdrew"
    event.registered_count -= 1
    db.session.commit()
    return "Successfully withdrew from the event"


# Create a new club
def create_club(club_information):
    if 'name' not in club_information or\
            'head' not in club_information or\
            'category' not in club_information or\
            'description' not in club_information:
        return (200, "Missing information(name, head, " +
                "category, description) required to create club")
    name = club_information['name']
    head = club_information['head']
    category = club_information['category']
    description = club_information['description']

    if club_exist(name):
        return 200, "Club with same name already exist"

    new_club = Club(name=name, head=head, category=category,
                    description=description)

    db.session.add(new_club)
    db.session.commit()

    student_id = get_id(head)
    club_id = get_club_id(name)
    role = "Club Head"

    new_role = Role(student_id=student_id, club_id=club_id, role=role)
    db.session.add(new_role)
    db.session.commit()

    return 200, "Club Entry Created"


# Gets the role of student for the clubs
# for which student is either a head or member of.
def get_roles(student_id):
    query = db.session.query(Role).filter_by(student_id=student_id)
    clubs_response = query.all()
    clubs_response.sort(key=lambda x: x.club_id)
    clubs = []
    for club in clubs_response:
        clubs.append(club.as_dict())
    return clubs
