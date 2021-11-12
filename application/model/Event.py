from application.controller.controllers import db


class Event(db.Model):
    __tablename__ = "event"

    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club._id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    visibility = db.Column(db.String(50), nullable=False)
    start_timestamp = db.Column(db.DateTime, nullable=False)
    end_timestamp = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    max_registration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    fee = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    registered_count = db.Column(db.Integer, nullable=False)

    def __init__(self, name, category, club_id, visibility, start_timestamp, end_timestamp, location, max_registration,
                 fee, status, registered_count, description=''):
        self.name = name
        self.category = category
        self.description = description
        self.club_id = club_id
        self.visibility = visibility
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.location = location
        self.max_registration = max_registration
        self.description = description
        self.fee = fee
        self.status = status
        self.registered_count = registered_count