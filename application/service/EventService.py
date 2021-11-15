from os import stat
from application.model.Event import Event
from application.model.Role import Role
from application.model.StudentEvent import StudentEvent
from application.service.StudentService import get_id as student_get_id
from application.utilities.database import db



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