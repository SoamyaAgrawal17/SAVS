from application.controller.controllers import db


class Role(db.Model):
    __tablename__ = "role"

    student_id = db.Column(db.Integer, db.ForeignKey('student._id', onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club._id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False, primary_key=True)
    role = db.Column(db.String(20), nullable=False)

    def __init__(self, student_id, club_id, role):
        self.student_id = student_id
        self.club_id = club_id
        self.role = role


