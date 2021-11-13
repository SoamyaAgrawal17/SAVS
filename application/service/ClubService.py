# from application.model.Club import Club
# from application.controller.controllers import db
# from application.model.Role import Role
# from application.model.Student import Student

def get_clubs():
    club_list = ["club1", "club2"]
    return club_list


def get_club(club_id):
    club = "club"
    return club


def edit_club(db, club, club_details):
    # update club
    for key,value in club_details.items():
        setattr(club,key,value)
    db.session.commit()
    print(club_details)    
    return "edited club"

def delete_club(db, club):
    # delete club
    db.session.delete(club)
    db.session.commit()
    return "club deleted"

def add_member(db,role):
    # student = Student.query.get(_id = student_id)
    # if student is None:
    #     return "error: student not found"
    # club = get_club(db,club_id)
    # if club is None:
    #     return "error: club not found"
    # db.session.add(Role(student_id = student_id, club_id = club_id, role = "member"))
    db.session.add(role)
    db.session.commit()
    return "member added"
