from application.utilities.database import db
from application.model.Club import Club
from application.model.Role import Role
from application.model.Student import Student


# get id for a club name
def get_id(club_name):
    club = db.session.query(Club).filter(Club.name.in_([club_name])).first()
    club_id = club._id
    return club_id


# check if a club with 'name' exists
def club_exist(name):
    query = db.session.query(Club).filter_by(name=name).all()
    return len(query) > 0


# get all registered clubs
def get_clubs():
    query = db.session.query(Club)
    results = query.all()
    clubs = []
    for res in results:
        clubs.append(res.as_dict())
    return clubs


# get club details corresponding to club_id
def get_club(club_id):
    query = db.session.query(Club).filter(Club._id.in_([club_id]))
    result = query.first()
    if result is None:
        return None
    return result.as_dict()


# edit club corresponding to club_id
# and set new club_details
def edit_club(club_id, club_details):
    # update club
    club = Club.query.get(club_id)
    if 'name' in club_details.keys():
        if club_details['name'] == '':
            return "club cannot have empty name"
    for key, value in club_details.items():
        setattr(club, key, value)
    db.session.commit()
    return "edited club"


# delete club corresponding to club_id
def delete_club(club_id):
    # delete club
    club = Club.query.filter_by(_id=club_id)
    if club is None:
        return "club does not exist"
    Club.query.filter_by(_id=club_id).delete()
    db.session.commit()
    return "club deleted"


# add member corresponding to student_id
# to the club corresponding to club_id
def add_member(club_id, student_id):
    student = Student.query.get(student_id)
    if student is None:
        return "error: student not found"
    club = Club.query.get(club_id)
    if club is None:
        return "error: club not found"
    db.session.add(Role(student_id=student_id, club_id=club_id,
                        role="Club Member"))
    db.session.commit()
    return "Club member added"

# remove member corresponding to student_id
# to the club corresponding to club_id
def remove_member(club_id, student_id):
    student = Student.query.get(student_id)
    if student is None:
        return "error: student not found"
    club = Club.query.get(club_id)
    if club is None:
        return "error: club not found"
    Role.query.filter(Role.student_id == student_id, Role.club_id == club_id).delete()
    db.session.commit()
    return "Club member has been removed"
