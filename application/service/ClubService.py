from application.utilities.database import db
from application.model.Club import Club
from application.model.Role import Role


def get_id(club_name):
    club = db.session.query(Club).filter(Club.name.in_([club_name])).first()
    club_id = club._id
    return club_id


def club_exist(name):
    query = db.session.query(Club).filter_by(name=name).all()
    return len(query) > 0


def get_clubs():
    query = db.session.query(Club)
    results = query.all()
    return results


def get_club(club_id):
    query = db.session.query(Club).filter(Club._id.in_([club_id]))
    result = query.first()
    return result.as_dict()


def edit_club(club_id,club_details):
    club = get_club(club_id)
    for key,value in club_details.items():
        setattr(club,key,value)
    db.session.commit() 
    return "edited club"


def delete_club(club_id):
    # delete club
    # Club.query.filter_by(_id=club_id).delete()
    club = get_club(club_id)
    db.session.delete(club)
    db.session.commit()
    return "club deleted"