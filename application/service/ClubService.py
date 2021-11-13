from application.model.Club import Club
from application.controller.controllers import db
from application.model.Role import Role
from application.model.Student import Student

def get_clubs():
    club_list = ["club1", "club2"]
    return club_list


def get_club(club_id):
    club = "club"
    return club


def edit_club(club_id, club_details):
    # update club
    club = get_club(db,club_id)
    for detail in club_details:
        if detail not in club:
            return "error: incorrect details"
        club[detail]=club_details[detail]
    db.session.commit()    
    return "edited club"

def delete_club(club_id):
    # delete club
    Club.query.filter_by(_id=club_id).delete()
    db.session.commit()

def add_member(club_id,student_id):
    student = Student.query.get(_id = student_id)
    if student is None:
        return "error: student not found"
    club = get_club(db,club_id)
    if club is None:
        return "error: club not found"
    db.session.add(Role(student_id = student_id, club_id = club_id, role = "member"))
    db.session.commit()

