from application.controller.controllers import db


class StudentEvents(db.Model):
    __tablename__ = "student_events"

    student_id = db.Column(db. Integer, db.ForeignKey('students._id', onupdate="CASCADE", ondelete="CASCADE"),
                           nullable=False, primary_key=True)
    event_id = db.Column(db. Integer, db.ForeignKey('events._id', onupdate="CASCADE", ondelete="CASCADE"),
                         nullable=False, primary_key=True)
    status = db.Column(db.String(100), nullable=True)

    def __init__(self, student_id, event_id, status=None):
        self.student_id = student_id
        self.event_id = event_id
        self.status = status