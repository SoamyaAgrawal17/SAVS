import datetime
import unittest
from application.service import EventService
from application.utilities.database import db
from app import app
from datetime import *

app.config['TESTING'] = True


class Test_TestEventService(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql://ganjvezplkwnyf:' \
            'c2ab9de3ce2ca931f13aa6e62667607ac5f19929425b7ef16a237fe' \
            '61c664d97@ec2-34-198-189-252.compute-1.amazonaws.com:5432/' \
            'dbjeqssrqgcj15'

        with app.app_context():
            db.init_app(app)
            from application.model import Club, Event, Role, Student
            db.create_all()
            db.session.commit()
            student1 = Student.Student(name="Bob", email_id="bob@abc.com",
                                       college="College1", department="CS")
            student1._id = 1
            student2 = Student.Student(name="Alice", email_id="alice@abc.com",
                                       college="College1", department="CS")
            student2._id = 2
            club1 = Club.Club(name="Club1", head="head@abc.com",
                              category="Sports", description="Description")
            club2 = Club.Club(name="Club2", head="head@abc.com",
                              category="Academic", description="Description")
            club1._id = 1
            club2._id = 2
            role1 = Role.Role(student_id=1, club_id=1, role="Club Member")
            role2 = Role.Role(student_id=2, club_id=1, role="Club Member")
            role3 = Role.Role(student_id=2, club_id=2, role="Club Member")
            event1 = Event.Event(name="Event1", category="Sports",
                                 description="Desc", club_id=1,
                                 visibility="Students",
                                 start_timestamp="2021-12-03 09:30:00",
                                 end_timestamp="2021-12-03 09:30:00",
                                 location="NYC", max_registration=50,
                                 fee=5, status="Approved",
                                 registered_count=50, created_by=1)
            event2 = Event.Event(name="Event2", category="Music",
                                 description="Musical Night", club_id=1,
                                 visibility="Students",
                                 start_timestamp="2021-12-03 09:30:00",
                                 end_timestamp="2021-12-03 09:30:00",
                                 location="CA", max_registration=50,
                                 fee=10, status="Proposed",
                                 registered_count=50, created_by=2)
            db.session.add(student1)
            db.session.add(student2)
            db.session.add(club1)
            db.session.add(club2)
            db.session.commit()

            db.session.add(role1)
            db.session.add(role2)
            db.session.add(role3)
            db.session.commit()

            db.session.add(event1)
            db.session.add(event2)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()

    def test_get_events(self):
        # Test if a list of events are returned
        with app.app_context():
            events = EventService.get_events()
            self.assertEqual(len(events), 2)
            self.assertEqual(events[0].name, "Event1")
            self.assertEqual(events[0].location, "NYC")
            self.assertEqual(events[0].description, "Desc")

    def test_get_events_created_by(self):
        # Test if the list of events returned were created by the user
        with app.app_context():
            events = EventService.get_events(created_by=1)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].name, "Event1")
            self.assertEqual(events[0].location, "NYC")
            self.assertEqual(events[0].description, "Desc")

    def test_get_filtered_events(self):

        with app.app_context():
            event_obj = {
                "name": "ICPC Practice 2021",
                "club_id": 1,
                "start_timestamp": "2021-12-25 09:30:00",
                "end_timestamp": "2021-12-26 09:30:00",
                "location": "New York City",
                "max_registration": 250,
                "description": "Competitive Coding Practice",
                "fee": 10,
                "category": "Academic"
            }

            msg, code = EventService.propose_event(event_obj, 1)
            self.assertEqual(msg, "CREATED")
            self.assertEqual(code, 201)
            events = EventService.get_events()
            self.assertEqual(len(events), 3)

            # Test if a list of events filtered by dates are returned
            filters = {"date_range": {"start": "2021-12-22 09:30:00", "end": "2021-12-27 09:30:00"}}
            events = EventService.get_filtered_events(filters)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].name, "ICPC Practice 2021")
            self.assertEqual(events[0].location, "New York City")
            self.assertEqual(events[0].description, "Competitive Coding Practice")

            # Test if a list of events filtered by fees are returned
            filters = {"fees": {"min": 0, "max": 7}}
            events = EventService.get_filtered_events(filters)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].name, "Event1")
            self.assertEqual(events[0].location, "NYC")
            self.assertEqual(events[0].description, "Desc")

            # Test if a list of events filtered by interests are returned
            filters = {"interests": "Music"}
            events = EventService.get_filtered_events(filters)
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0].name, "Event2")
            self.assertEqual(events[0].location, "CA")
            self.assertEqual(events[0].description, "Musical Night")

    def test_add_event(self):
        # Test if an event can be added by Club Member
        with app.app_context():
            event_obj = {
                "name": "ICPC Practice 2021",
                "club_id": 1,
                "start_timestamp": "2021-12-03 09:30:00",
                "end_timestamp": "021-12-05 00:00:00",
                "location": "New York City",
                "max_registration": 250,
                "description": "Competitive Coding Practice",
                "fee": 5,
                "category": "Academic"
            }

            msg, code = EventService.propose_event(event_obj, 1)
            self.assertEqual(msg, "CREATED")
            self.assertEqual(code, 201)
            events = EventService.get_events()
            self.assertEqual(len(events), 3)

    def test_add_event_unauthorized(self):
        '''
        Test if error is returned if a user tries to add an event
        for a club for which the user is not a member or head
        '''
        with app.app_context():
            event_obj = {
                "name": "ICPC Practice 2021",
                "club_id": 1,
                "start_timestamp": "2021-12-03 09:30:00",
                "end_timestamp": "021-12-05 00:00:00",
                "location": "New York City",
                "max_registration": 250,
                "description": "Competitive Coding Practice",
                "fee": 5,
                "category": "Academic"
            }

            msg, code = EventService.propose_event(event_obj, 3)
            self.assertEqual(msg, "You do not have the required"
                                  " permissions to perform this operation")
            self.assertEqual(code, 403)
            events = EventService.get_events()
            self.assertEqual(len(events), 2)

    def test_edit_events(self):
        # Test if an event can be edited by Club Member
        with app.app_context():
            event_obj = {
                "name": "Event Title",
                "club_id": 1,
                "start_timestamp": "2021-12-03 09:30:00",
                "end_timestamp": "2021-12-05 00:00:00",
                "location": "NJ",
                "max_registration": 75,
                "description": "Tennis",
                "category": "Sports"
            }

            msg, code = EventService.edit_event(event_obj, 1, 1)
            event = EventService.get_event(1)
            self.assertEqual(msg, "CREATED")
            self.assertEqual(code, 201)
            self.assertEqual(event.name, "Event Title")
            self.assertEqual(event.location, "NJ")
            self.assertEqual(event.description, "Tennis")

    def test_edit_events_unauthorized(self):
        '''
        Test if error is returned if a user tries to edit an event
        for a club for which the user is not a member or head
        '''
        with app.app_context():
            event_obj = {
                "name": "Event Title",
                "club_id": 1,
                "start_timestamp": "2021-12-03 09:30:00",
                "end_timestamp": "021-12-05 00:00:00",
                "location": "NJ",
                "max_registration": 75,
                "description": "Tennis",
                "category": "Sports"
            }

            msg, code = EventService.edit_event(event_obj, 1, 3)
            event = EventService.get_event(1)
            self.assertEqual(msg, "You do not have the required"
                                  " permissions to perform this operation")
            self.assertEqual(code, 403)
            self.assertEqual(event.name, "Event1")
            self.assertEqual(event.location, "NYC")

    def test_edit_events_forbidden_fields_approved(self):
        with app.app_context():
            event_obj = {
                "name": "Event Title",
                "club_id": 1,
                "start_timestamp": "2021-12-03 09:30:00",
                "end_timestamp": "021-12-05 00:00:00",
                "location": "NJ",
                "max_registration": 75,
                "description": "Tennis",
                "category": "Sports",
                "fee": 12
            }

            msg, code = EventService.edit_event(event_obj, 1, 1)
            event = EventService.get_event(1)
            self.assertEqual(msg, "You cannot edit forbidden fields: fee")
            self.assertEqual(code, 500)
            self.assertEqual(event.name, "Event1")
            self.assertEqual(event.location, "NYC")

    def test_edit_events_forbidden_fields_proposed(self):
        with app.app_context():
            event_obj = {
                "name": "Event Title",
                "club_id": 1,
                "start_timestamp": "2021-12-03 09:30:00",
                "end_timestamp": "021-12-05 00:00:00",
                "location": "NJ",
                "max_registration": 75,
                "description": "Tennis",
                "category": "Sports",
                "fee": 12,
                "registered_count": 25
            }

            msg, code = EventService.edit_event(event_obj, 2, 2)
            event = EventService.get_event(2)
            self.assertEqual(msg, "You cannot edit forbidden fields: registered_count")
            self.assertEqual(code, 500)
            self.assertEqual(event.name, "Event2")
            self.assertEqual(event.location, "CA")

    def test_edit_past_events(self):
        with app.app_context():
            from application.model import Event
            event3 = Event.Event(name="Event3", category="Academic",
                                 description="Hackathon", club_id=1,
                                 visibility="Students",
                                 start_timestamp="2020-12-03 09:30:00",
                                 end_timestamp="2020-12-03 09:30:00",
                                 location="SF", max_registration=100,
                                 fee=10, status="Approved",
                                 registered_count=100, created_by=2)
            db.session.add(event3)
            db.session.commit()
            event_obj = {
                "name": "New Hackathon",
                "club_id": 1,
                "location": "CA",
                "max_registration": 75,
            }

            msg, code = EventService.edit_event(event_obj, 3, 2)
            event = EventService.get_event(3)
            self.assertEqual(msg, "Cannot edit past events")
            self.assertEqual(code, 500)
            self.assertEqual(event.name, "Event3")
            self.assertEqual(event.location, "SF")

    def test_edit_rejected_events(self):
        with app.app_context():
            from application.model import Event
            event3 = Event.Event(name="Event3", category="Academic",
                                 description="Hackathon", club_id=1,
                                 visibility="Students",
                                 start_timestamp="2025-12-03 09:30:00",
                                 end_timestamp="2025-12-03 09:30:00",
                                 location="SF", max_registration=100,
                                 fee=10, status="Rejected",
                                 registered_count=100, created_by=2)
            db.session.add(event3)
            db.session.commit()
            event_obj = {
                "name": "New Hackathon",
                "club_id": 1,
                "location": "CA",
                "max_registration": 75,
            }

            msg, code = EventService.edit_event(event_obj, 3, 2)
            event = EventService.get_event(3)
            self.assertEqual(msg, "You cannot edit Rejected Events")
            self.assertEqual(code, 500)
            self.assertEqual(event.name, "Event3")
            self.assertEqual(event.location, "SF")

    def test_edit_club_id(self):
        with app.app_context():
            from application.model import Event
            event3 = Event.Event(name="Event3", category="Academic",
                                 description="Hackathon", club_id=2,
                                 visibility="Students",
                                 start_timestamp="2025-12-03 09:30:00",
                                 end_timestamp="2025-12-03 09:30:00",
                                 location="SF", max_registration=100,
                                 fee=10, status="Proposed",
                                 registered_count=100, created_by=2)
            db.session.add(event3)
            db.session.commit()
            event_obj = {
                "name": "New Hackathon",
                "club_id": 1,
                "location": "CA",
                "max_registration": 75,
            }

            msg, code = EventService.edit_event(event_obj, 3, 2)
            event = EventService.get_event(3)
            self.assertEqual(msg, "You cannot edit club id of event")
            self.assertEqual(code, 500)
            self.assertEqual(event.name, "Event3")
            self.assertEqual(event.location, "SF")



if __name__ == '__main__':
    unittest.main()