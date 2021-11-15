from application.utilities.database import db


class Club(db.Model):
    __tablename__ = "club"


    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    head = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=True)

    def __init__(self, name, head, category, description):
        self.name = name
        self.head = head
        self.category = category
        self.description = description
