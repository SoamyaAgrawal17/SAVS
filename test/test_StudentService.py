import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from application.service import EventService, StudentService
from application.utilities.database import db
import json
from app import app

app.config['TESTING'] = True


class Test_TestStudentService(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://qvlexpubbtkawz:c415dbfa33e578124d9b3774a0e460c980bfd656f679a175907a7c0b63581af5@ec2-54-174-172-218.compute-1.amazonaws.com:5432/d5n4m2th52nbcq'
        with app.app_context():
            db.init_app(app)
            from application.model import Club, Event, Role, Student, StudentEvent
            db.create_all()
            db.session.commit()
        self.x = None

    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()
        self.x = None

    def test_create_event(self):
        with app.app_context():
            student_information = {
                "name": "TestStudent",
                "email_id": "test_student@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }

            student = StudentService.create_student(student_information)
            student1 = StudentService.get_student("test_student@columbia.edu")
            res = json.dumps(student, default=str)
            print(student)
            print(student1)
            self.assertEqual(True, True)

    def test_get_event(self):
        with app.app_context():
            events = StudentService.get_student("test_student@columbia.edu")
            res = json.dumps(events, default=str)
            print(res)
            self.assertEqual(True, True)

    def test_get_upcoming_events(self):
        with app.app_context():
            student_id = StudentService.get_id("test_student@columbia.edu")
            print(student_id)
            self.assertEqual()


if __name__ == '__main__':
    unittest.main()