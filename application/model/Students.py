from application.controller.controllers import db


class Students(db.Model):
    __tablename__ = "students"

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
