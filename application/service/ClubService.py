from application.utilities.database import db
from application.model.Club import Club
from application.model.Role import Role
from application.model.Student import Student
# from application.service.StudentService import get_id as get_student_id


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
def edit_club(email_id, club_id, club_details):
    # update club
    res, code = verify_club_head(email_id, club_id)
    if code != 200:
        return res, code
    club = Club.query.get(club_id)
    if 'name' in club_details.keys():
        if club_details['name'] == '':
            return "club cannot have empty name", 400
    for key, value in club_details.items():
        setattr(club, key, value)
    db.session.commit()
    return "edited club", 200


# update club head corresponding to club_id
def assign_successor(email_id, club_id, club_head_email):
    # assign new head
    res, code = verify_club_head(email_id, club_id)
    if code != 200:
        return res, code
    club = Club.query.get(club_id)
    old_head_id = get_student_id(email_id)
    new_head_id = get_student_id(club_head_email)
    if new_head_id == "Student does not exist":
        return "error: student isn't registered", 400
    Role.query.filter(Role.student_id == old_head_id,
                      Role.club_id == club_id).delete()
    setattr(club, 'head', club_head_email)
    role = Role(student_id=new_head_id, club_id=club_id, role="Club Head")
    db.session.add(role)
    db.session.commit()
    return "replaced successor", 200


# delete club corresponding to club_id
def delete_club(email_id, club_id):
    # delete club
    res, code = verify_club_head(email_id, club_id)
    if code != 200:
        return res, code
    Club.query.filter_by(_id=club_id).delete()
    db.session.commit()
    return "club deleted", 200


# add member corresponding to student_id
# to the club corresponding to club_id
def add_member(email_id, club_id, student_email_id):
    res, code = verify_club_head(email_id, club_id)
    if code != 200:
        return res, code
    student_id = get_student_id(student_email_id)
    if student_id == "Student does not exist":
        return "error: student isn't registered", 400
    db.session.add(Role(student_id=student_id, club_id=club_id,
                        role="Club Member"))
    db.session.commit()
    return "Club member added", 200


# remove member corresponding to student_id
# to the club corresponding to club_id
def remove_member(email_id, club_id, student_email_id):
    res, code = verify_club_head(email_id, club_id)
    if code != 200:
        return res, code
    student_id = get_student_id(student_email_id)
    if student_id == "Student does not exist":
        return "error: student isn't registered", 400
    Role.query.filter(Role.student_id == student_id,
                      Role.club_id == club_id).delete()
    db.session.commit()
    return "Club member has been removed", 200


# verify that the club and club head
# information is accurate
def verify_club_head(email_id, club_id):
    club = Club.query.get(club_id)
    if club is None:
        return "club does not exist", 400
    if email_id is None:
        return "Invalid Request", 400

    student_id = get_student_id(email_id)

    if student_id == "Student does not exist":
        return "Invalid Request", 400

    query = Role.query.filter_by(club_id=club_id, student_id=student_id)
    result = query.first()

    if result is None or result.role != "Club Head":
        return "Invalid Request", 400
    return "Valid request", 200


# get student id given student email
# we cannot depend on student service to avoid circular dependency
def get_student_id(email_id):
    student = Student.query.filter_by(email_id=email_id).first()
    if student is None:
        return "Student does not exist"
    student_id = student._id
    return student_id
