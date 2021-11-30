from application.model.Student import Student
from application.model.Event import Event
from application.model.StudentEvent import StudentEvent
from application.model.Role import Role
from application.model.Club import Club
from application.utilities.database import db


def clear_database():
    db.session.query(Role).delete()
    db.session.query(StudentEvent).delete()
    db.session.query(Club).delete()
    db.session.query(Student).delete()
    db.session.query(Event).delete()
    db.session.execute("alter sequence club__id_seq restart 1")
    db.session.execute("alter sequence student__id_seq restart 1")
    db.session.execute("alter sequence event__id_seq restart 1")
    db.session.commit()
    return "Cleared database"
