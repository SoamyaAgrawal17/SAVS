import unittest
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

sys.path.append('../SAVS')
from application.model.Club import Club
from application.model.Event import Event
from application.model.Role import Role
from application.model.StudentEvent import StudentEvent
from application.model.Student import Student


test_app = Flask(__name__)
test_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
test_app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kzvwdrxlhzlukx:431c5a2e7ec9f2ae924ff6cd73ce36e3053de8b591b312c43b221c95a9d2f920@ec2-52-204-72-14.compute-1.amazonaws.com:5432/dd1houemgk2i24'

class Test_TestEventService(unittest.TestCase):
    def setUp(self):
        print("Running setup")
        self.x = None
        self.db = SQLAlchemy()
        self.db.init_app(test_app)
        self.db.create_all()
        self.db.session.commit()

    def tearDown(self):
        print("Running tear down")
        self.x = None

    def test_sample(self):
        print("Running test sample")
        self.assertEqual(True, True)


if __name__ == '_main_':
    print("main",sys="")
    t = Test_TestEventService()
    t.setUp()
    unittest.main()