from application.utilities.database import db


class Student(db.Model):
    __tablename__ = "student"

    _id = db.Column(db. Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email_id = db.Column(db.String(100), nullable=False)
    college = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email_id, college, department):
        self.name = name
        self.email_id = email_id
        self.college = college
        self.department = department

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
