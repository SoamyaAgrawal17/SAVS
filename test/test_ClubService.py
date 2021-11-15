import unittest

# from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.model.Club import Club
from flask import Flask, request, jsonify, Response, render_template, request
from application.model.Event import Event
from application.model.Role import Role
from application.model.StudentEvent import StudentEvent
from application.model.Student import Student
from application.service import ClubService
from application.controller import ClubsController

test_app = Flask(__name__)
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kzvwdrxlhzlukx:431c5a2e7ec9f2ae924ff6cd73ce36e3053de8b591b312c43b221c95a9d2f920@ec2-52-204-72-14.compute-1.amazonaws.com:5432/dd1houemgk2i24'

blueprints = [
    ClubsController.mod
]

for bp in blueprints:
    test_app.register_blueprint(bp)

class Test_TestClubService(unittest.TestCase):
    def setUp(self):
        self.x = None
        self.db = SQLAlchemy()
        self.db.init_app(test_app)
        # with test_app.app_context():
        #     from application.model.Club import Club
        #     from application.model.Event import Event
        #     from application.model.Role import Role
        #     from application.model.StudentEvent import StudentEvent
        #     from application.model.Student import Student
        #     print("setup")
        #     self.db.create_all()
        #     self.db.session.commit()




    def test_getclub(self):
        print("whatever")
        with test_app.app_context():
            # query = Club.query.get(2)
            # results = query.one()
            results = ClubService.get_club(1)
            print(results)
        self.setUp()
        self.assertEqual(True, True)


    def tearDown(self):
        self.db = None


if __name__ == '__main__':
    unittest.main()