from application.utilities.database import db
from flask import Flask
from application.controller import ClubsController, EventsController
from application.controller import StudentsController

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kzvwdrxlhzlukx:431c5a2e7ec9f2ae924ff6cd73ce36e3053de8b591b312c43b221c95a9d2f920@ec2-52-204-72-14.compute-1.amazonaws.com:5432/dd1houemgk2i24'


blueprints = [
    ClubsController.mod,
    StudentsController.mod,
    EventsController.mod
]

for bp in blueprints:
    app.register_blueprint(bp)

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)