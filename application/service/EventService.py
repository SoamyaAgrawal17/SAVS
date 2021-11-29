import datetime

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
    event_list.sort(key=lambda x: x._id)
    return event_list


# Get list of events based on filters
def get_filtered_events(filters=None):

    query = db.session.query(Event)
    event_list = query.all()

    date_filtered_events = []
    if "date_range" in filters:
        for event in event_list:
            event_timestamp = event.start_timestamp
            start_date = datetime.datetime.strptime(filters["date_range"]["start"], "%Y-%m-%d %H:%M:%S")
            end_date = datetime.datetime.strptime(filters["date_range"]["end"], "%Y-%m-%d %H:%M:%S")
            if event_timestamp >= start_date and event_timestamp <= end_date:
                date_filtered_events.append(event)

    # Filter by fee range
    fee_filtered_events = []
    if "fees" in filters:
        for event in event_list:
            if event.fee >= filters["fees"]["min"] and event.fee <= filters["fees"]["max"]:
                fee_filtered_events.append(event)

    # Filter by interests
    interest_filtered_events = []
    if "interests" in filters:
        for event in event_list:
            if event.category == filters["interests"]:
                interest_filtered_events.append(event)

    # Filter by clubs
    club_filtered_events = []
    if "clubs" in filters:
        for event in event_list:
            if event.club_id == filters["clubs"]:
                club_filtered_events.append(event)

    return tuple(set(date_filtered_events + fee_filtered_events + interest_filtered_events + club_filtered_events))
    # return list(set.union((date_filtered_events, fee_filtered_events, interest_filtered_events, club_filtered_events)))


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
        if 'visibility' not in event_information:
            visibility = "Club Member"
        else:
            visibility = event_information['visibility']
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
    event = get_event(event_id)
    if event.get_time_status_() == "Past":
        message = "Cannot edit past events"
        status_code = 500
        return message, status_code

    '''
    if event.created_by != student_id:
        message = "You cannot edit events not proposed by you"
        status_code = 403
        return message, status_code
    '''

    event_status = event.status
    proposed_prohibited = ["registered_count", "created_by"]
    approved_prohibited = ["visibility", "fee", "created_by", "registered_count"]

    if event_status == "Proposed" or event_status == "Approved":
        if event.club_id != club_id:
            message = "You cannot edit club id of event"
            status_code = 500
            return message, status_code
        field_list = []
        check_fields = proposed_prohibited if event_status == "Proposed" else approved_prohibited
        for key in check_fields:
            if key in event_information:
                field_list.append(key)
        if len(field_list) > 0:
            message = "You cannot edit forbidden fields: " + ', '.join(field_list)
            status_code = 500
            return message, status_code
    else:
        message = "You cannot edit Rejected Events"
        status_code = 500
        return message, status_code

    if role == "Club Member" or role == "Club Head":
        event_edit = db.session.query(Event).filter(Event._id.in_(
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
