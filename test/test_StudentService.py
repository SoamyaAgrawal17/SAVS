import unittest

from application.service import StudentService, EventService
from application.utilities.database import db
from app import app

app.config['TESTING'] = True
email_id = "test_student@columbia.edu"
email_id_1 = "test_student1@columbia.edu"
email_id_2 = "test_student2@columbia.edu"
student_registered_for_event = "Student registered for the event"
club_member = "Club Member"
event_description = "Winter Hackathon December 2021"
event_location = "New York City"
event_name = "Hackathon 2021 Columbia"
test_club_member = "test_club_member@columbia.edu"
college_name = "Fu Foundation"
department_name = "Computer Science"
club_description_2 = "Test Club Description 2"
club_3 = "Test Club 3"
category_2 = "Test Category 2"
club_entry_created = "Club Entry Created"


class test_student_service(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql://qvlexpubbtkawz:c415dbfa33e578124d9b3774' \
            'a0e460c980bfd656f679a175907a7c0b63581af5@ec2-54-174-17' \
            '2-218.compute-1.amazonaws.com:5432/d5n4m2th52nbcq'
        with app.app_context():
            db.init_app(app)
            db.create_all()
            db.session.commit()
        self.x = None

    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()
        self.x = None

    def test_register_event_and_registered_events(self):
        # Test if a student can register for events
        with app.app_context():
            student_information = {
                "email_id": email_id,
                "college": college_name,
                "department": department_name
            }

            response = StudentService.create_student(student_information)
            self.assertEqual(response,
                             "Missing information(name, email_id, " +
                             "college, department) required to create student")

            student_information = {
                "name": "TestStudent",
                "email_id": email_id,
                "college": college_name,
                "department": department_name
            }

            StudentService.create_student(student_information)
            student_id = StudentService.get_student(
                email_id)['_id']
            self.assertEqual(student_id, 1)

            club_information = {
                "name": club_3,
                "head": email_id,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(status, 200)
            self.assertEqual(response, club_entry_created)

            event = {
                "emailId": test_club_member,
                "event": {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2021-12-26 09:30:00",
                    "end_timestamp": "2021-12-27 00:00:00",
                    "location": event_location,
                    "max_registration": 125,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": club_member,
                    "status": "Created"
                }
            }

            EventService.propose_event(event['event'], student_id)
            event_id = 1
            registration = StudentService.register_event(event_id, student_id)
            self.assertEqual(registration, student_registered_for_event)

            # Register in an event
            registration = StudentService.register_event(event_id, student_id)
            self.assertEqual(registration, "Student already " +
                                           "registered for the event")
            registered_events = StudentService.\
                get_registered_events(student_id)
            registered_event = registered_events[0]
            self.assertEqual(registered_event['student_id'], 1)
            self.assertEqual(registered_event['event']['_id'], 1)
            self.assertEqual(registered_event['event']['registered_count'], 1)
            self.assertEqual(registered_event['status'], "Registered")

            # Withdraw from a registered event
            response = StudentService.withdraw_event(event_id, student_id)
            self.assertEqual(response, "Successfully withdrew from the event")
            registered_events = StudentService.\
                get_registered_events(student_id)
            registered_event = registered_events[0]
            self.assertEqual(registered_event['event']['_id'], 1)
            self.assertEqual(registered_event['event']['registered_count'], 0)
            self.assertEqual(registered_event['student_id'], 1)
            self.assertEqual(registered_event['status'], "Withdrew")

            # Withdraw from an event not registered in
            response = StudentService.withdraw_event(3, student_id)
            self.assertEqual(response,
                             "Failure: Can't withdraw " +
                             "from an event not registered in")

    def test_withdraw_from_past_event(self):
        # Test if a student can register for events
        with app.app_context():
            student_information = {
                "name": "TestStudent",
                "email_id": email_id,
                "college": college_name,
                "department": department_name
            }

            StudentService.create_student(student_information)
            student_id = StudentService.get_student(
                email_id)['_id']
            self.assertEqual(student_id, 1)

            club_information = {
                "name": club_3,
                "head": email_id,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(status, 200)
            self.assertEqual(response, club_entry_created)

            event = {
                "emailId": test_club_member,
                "event": {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2021-12-26 09:30:00",
                    "end_timestamp": "2021-12-27 00:00:00",
                    "location": event_location,
                    "max_registration": 125,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": club_member,
                    "status": "Created"
                }
            }

            EventService.propose_event(event['event'], student_id)
            event_id = 1
            registration = StudentService.register_event(event_id, student_id)
            self.assertEqual(registration, student_registered_for_event)

            # Register in an event
            registration = StudentService.register_event(event_id, student_id)
            self.assertEqual(registration, "Student already " +
                                           "registered for the event")
            registered_events = StudentService.\
                get_registered_events(student_id)
            registered_event = registered_events[0]
            self.assertEqual(registered_event['student_id'], 1)
            self.assertEqual(registered_event['event']['_id'], 1)
            self.assertEqual(registered_event['event']['registered_count'], 1)
            self.assertEqual(registered_event['status'], "Registered")

            event_information = {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2020-12-26 09:30:00",
                    "end_timestamp": "2020-12-27 00:00:00",
                    "location": event_location,
                    "max_registration": 125,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": club_member,
                }

            EventService.edit_event(event_information, event_id, student_id)
            # Withdraw from a registered event
            response = StudentService.withdraw_event(event_id, student_id)
            self.assertEqual(response,
                             "Failure: Can't withdraw from past event")

    def test_register_past_events(self):
        # Test if a student can register for events
        with app.app_context():
            student_information = {
                "name": "TestStudent",
                "email_id": email_id,
                "college": college_name,
                "department": department_name
            }

            StudentService.create_student(student_information)
            student_id = StudentService.get_student(
                email_id)['_id']
            self.assertEqual(student_id, 1)

            club_information = {
                "name": club_3,
                "head": email_id,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(status, 200)
            self.assertEqual(response, club_entry_created)

            event = {
                "emailId": test_club_member,
                "event": {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2020-12-03 09:30:00",
                    "end_timestamp": "2020-12-05 00:00:00",
                    "location": event_location,
                    "max_registration": 125,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": "all",
                    "status": "Created"
                }
            }

            EventService.propose_event(event['event'], student_id)
            event_id = 1
            registration = StudentService.register_event(event_id, student_id)
            self.assertEqual(registration,
                             "You cannot register for an event in the past")

    def test_register_max_students(self):
        # Test if a student can register for events
        with app.app_context():
            student_information1 = {
                "name": "TestStudent",
                "email_id": email_id_1,
                "college": college_name,
                "department": department_name
            }

            student_information2 = {
                "name": "TestStudent2",
                "email_id": email_id_2,
                "college": college_name,
                "department": department_name
            }

            student_information3 = {
                "name": "TestStudent3",
                "email_id": "test_student3@columbia.edu",
                "college": college_name,
                "department": department_name
            }

            StudentService.create_student(student_information1)
            StudentService.create_student(student_information2)
            StudentService.create_student(student_information3)
            student_id1 = StudentService.get_student(
                email_id_1)['_id']
            self.assertEqual(student_id1, 1)
            student_id2 = StudentService.get_student(
                email_id_2)['_id']
            self.assertEqual(student_id2, 2)
            student_id3 = StudentService.get_student(
                "test_student3@columbia.edu")['_id']
            self.assertEqual(student_id3, 3)

            club_information = {
                "name": club_3,
                "head": email_id_1,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(status, 200)
            self.assertEqual(response, club_entry_created)

            event = {
                "emailId": test_club_member,
                "event": {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2021-12-23 09:30:00",
                    "end_timestamp": "2021-12-25 00:00:00",
                    "location": event_location,
                    "max_registration": 2,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": "All",
                    "status": "Created"
                }
            }

            EventService.propose_event(event['event'], student_id1)
            event_id = 1
            registration = StudentService.register_event(event_id, student_id1)
            self.assertEqual(registration, student_registered_for_event)

            registration = StudentService.register_event(event_id, student_id2)
            self.assertEqual(registration, student_registered_for_event)

            registration = StudentService.register_event(event_id, student_id3)
            self.assertEqual(registration, "The event is at maximum capacity")
            event2 = {
                "emailId": test_club_member,
                "event": {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2021-12-23 09:30:00",
                    "end_timestamp": "2021-12-25 00:00:00",
                    "location": event_location,
                    "max_registration": 2,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": club_member,
                    "status": "Created"
                }
            }
            EventService.propose_event(event2['event'], student_id1)
            event_id = 2
            registration = StudentService.register_event(event_id, student_id3)
            self.assertEqual(registration,
                             "You need to be part of " +
                             "this club to register for this event.")

    def test_create_new_club_and_role_in_it(self):
        # Test if a student can create a new club
        with app.app_context():
            student = {
                "name": "TestStudent2",
                "email_id": email_id_2,
                "college": college_name,
                "department": department_name
            }
            response = StudentService.create_student(student)
            self.assertEqual(response, "Student Entry Created")
            response = StudentService.create_student(student)
            self.assertEqual(response, "Student Already Exists")

            student_id = StudentService.get_student(
                email_id_2)['_id']
            self.assertEqual(student_id, 1)

            club_information = {
                "name": club_3,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(response,
                             "Missing information(name, " +
                             "head, category, description) " +
                             "required to create club")
            self.assertEqual(status, 200)

            club_information = {
                "name": club_3,
                "head": email_id_2,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(response, club_entry_created)
            self.assertEqual(status, 200)

            status, response = StudentService.create_club(club_information)
            self.assertEqual(response, "Club with same name already exist")
            self.assertEqual(status, 200)

            clubs = StudentService.get_roles(student_id)
            self.assertEqual(len(clubs), 1)
            club = clubs[0]
            self.assertEqual(club['role'], "Club Head")
            self.assertEqual(club['student_id'], student_id)

    def test_get_all_upcoming_events(self):
        # Test if all upcoming events are returned for a student
        with app.app_context():
            student_information = {
                "name": "TestStudent",
                "email_id": email_id,
                "college": college_name,
                "department": department_name
            }

            StudentService.create_student(student_information)
            student_id = StudentService.get_student(
                email_id)['_id']
            self.assertEqual(student_id, 1)
            student_id = StudentService.get_id(email_id)
            self.assertEqual(student_id, 1)
            response = StudentService.get_id(
                        "test_unregistered_student@columbia.edu")
            self.assertEqual(response, "Student does not exist")

            club_information = {
                "name": club_3,
                "head": email_id,
                "category": category_2,
                "description": club_description_2
            }
            status, response = StudentService.create_club(club_information)
            self.assertEqual(status, 200)
            self.assertEqual(response, club_entry_created)

            event = {
                "emailId": test_club_member,
                "event": {
                    "name": event_name,
                    "club_id": 1,
                    "start_timestamp": "2022-12-03 09:30:00",
                    "end_timestamp": "2022-12-05 00:00:00",
                    "location": event_location,
                    "max_registration": 125,
                    "description": event_description,
                    "fee": 10,
                    "category": "Academic",
                    "visibility": "all",
                    "status": "Created"
                }
            }

            EventService.propose_event(event['event'], student_id)
            event_id = 1
            StudentService.register_event(event_id, student_id)
            upcoming_events = StudentService. \
                get_upcoming_events(1)
            self.assertEqual(len(upcoming_events), 1)
            upcoming_event = upcoming_events[0]
            self.assertEqual(upcoming_event['_id'], 1)
            self.assertEqual(upcoming_event["name"], event_name)


if __name__ == '__main__':
    unittest.main()
