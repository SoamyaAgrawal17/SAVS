from application.model.Event import Event
from application.model.Role import Role
from application.utilities.database import db


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
