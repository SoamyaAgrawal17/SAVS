import unittest

from application.model.Role import Role
from application.service import ClubService
from application.service import StudentService
from application.utilities.database import db
from app import app

app.config["TESTING"] = True


class Test_TestClubService(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgresql://ganjvezplkwnyf:'\
            'c2ab9de3ce2ca931f13aa6e62667607ac5f19929425b7ef16a237fe61c664d97'\
            '@ec2-34-198-189-252.compute-1.amazonaws.com:5432/dbjeqssrqgcj15'
        with app.app_context():
            db.init_app(app)
            db.drop_all()
            db.session.commit()
            db.create_all()
            db.session.commit()
            # setup a demo student as club head
            student_information = {
                "name": "TestStudent",
                "email_id": "test_student@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            # setup a demo club
            club_information = {
                "name": "TestClub",
                "head": "test_student@columbia.edu",
                "category": "TestCategory",
                "description": "TestDescription"
            }
            StudentService.create_student(student_information)
            StudentService.create_club(club_information)
            db.session.commit()

    def test_editClub(self):
        # Test if a new club can be added
        with app.app_context():
            new_club_information = {
                "name": "NewTestClub",
                "category": "NewTestCategory",
                "description": "NewTestDescription"
            }
            club_id = 1
            result = ClubService.edit_club(club_id, new_club_information)
            club = ClubService.get_club(club_id)
            for key, value in new_club_information.items():
                self.assertEqual(club[key], value)
            self.assertEqual(result, "edited club")

    def test_deleteClub(self):
        # Test if a club can be deleted
        with app.app_context():
            club_id = 1
            result = ClubService.delete_club(club_id)
            self.assertEqual(result, "club deleted")
            club = ClubService.get_club(club_id)
            self.assertIsNone(club)

    def test_addClubMember(self):
        # Test if a club member can be added
        with app.app_context():
            club_id = 1
            member_information = {
                "name": "TestMember",
                "email_id": "test_member@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(member_information)
            student_id = StudentService.get_id(member_information["email_id"])
            result = ClubService.add_member(club_id, student_id)
            self.assertEqual(result, "Club member added")
            role = Role.query.filter_by(student_id=student_id, club_id=club_id)
            self.assertEqual(role.first().role, "Club Member")

    def test_getClubs(self):
        # Test if a list of club is returned
        with app.app_context():
            student_information = {
                "name": "TestStudent2",
                "email_id": "test_student2@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            club_information = {
                "name": "TestClub2",
                "head": "test_student@columbia.edu",
                "category": "TestCategory2",
                "description": "TestDescription2"
            }
            StudentService.create_student(student_information)
            StudentService.create_club(club_information)
            clubs = ClubService.get_clubs()
            self.assertEqual(len(clubs), 2)

    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
