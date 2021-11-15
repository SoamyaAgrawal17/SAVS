from application.utilities.database import db
from application.model.Club import Club
from application.model.Role import Role
from application.service.StudentService import get_id as student_get_id

def get_clubs():
    query = db.session.query(Club)
    results = query.all()
    return results


def get_club(club_id):
    query = db.session.query(Club).filter(Club._id.in_([club_id]))
    results = query.all()
    return results


def edit_club(club_id,club_details):
    club = get_club(club_id)
    for key,value in club_details.items():
        setattr(club,key,value)
    db.session.commit() 
    return "edited club"

# Create new student entry
def create_club(club_information):

    name = club_information['name']
    head = club_information['head']
    category = club_information['category']
    description = club_information['description']

    new_club = Club(name=name, head=head, category=category, description=description)
    
    db.session.add(new_club)
    db.session.commit()

    student_id = student_get_id(head)
    club_id = get_club_id(name)
    role = "Club Head"
    new_role = Role(student_id=student_id, club_id=club_id, role=role)
    db.session.add(new_role)
    db.session.commit()

    return "Club Entry Created"

def get_all_clubs(student_id):
    query = db.session.query(Role).filter_by(student_id=student_id)
    clubs = query.all()
    
    return clubs

def get_club_id(club_name):
    club = db.session.query(Club).filter(Club.name.in_([club_name])).first()
    club_id = club._id
    return club_id

def delete_club(club_id):
    # delete club
    # Club.query.filter_by(_id=club_id).delete()
    club = get_club(club_id)
    db.session.delete(club)
    db.session.commit()
    return "club deleted"