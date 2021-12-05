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
            student_information_2 = {
                "name": "TestStudent2",
                "email_id": "test_student_2@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }

            StudentService.create_student(student_information)
            StudentService.create_club(club_information)
            StudentService.create_student(student_information_2)

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
            result, code = ClubService.edit_club(
                "test_student@columbia.edu", club_id, new_club_information)
            club = ClubService.get_club(club_id)
            for key, value in new_club_information.items():
                self.assertEqual(club[key], value)
            self.assertEqual(result, "edited club")

    def test_invalid_editClub(self):
        # Test if any one other than head tries editing club
        with app.app_context():
            new_club_information = {
                "name": "NewTestClub",
                "category": "NewTestCategory",
                "description": "NewTestDescription"
            }
            old_club_information = {
                "name": "TestClub",
                "category": "TestCategory",
                "description": "TestDescription"
            }
            club_id = 1
            result, code = ClubService.edit_club(
                "test_student_2@columbia.edu", club_id, new_club_information)
            club = ClubService.get_club(club_id)
            for key, value in old_club_information.items():
                self.assertEqual(club[key], value)
            self.assertEqual(result, "Invalid Request")

    def test_invalid_editClub_2(self):
        # Test if name of club is given empty
        with app.app_context():
            new_club_information = {
                "name": "",
                "category": "NewTestCategory",
                "description": "NewTestDescription"
            }
            club_id = 1
            result, code = ClubService.edit_club(
                "test_student@columbia.edu", club_id, new_club_information)
            self.assertEqual(result, "club cannot have empty name")

    def test_invalid_editClub_3(self):
        # Test if a new club can be edited without name
        with app.app_context():
            new_club_information = {
                "category": "NewTestCategory",
                "description": "NewTestDescription"
            }
            club_id = 1
            result, code = ClubService.edit_club(
                "test_student@columbia.edu", club_id, new_club_information)
            club = ClubService.get_club(club_id)
            for key, value in new_club_information.items():
                self.assertEqual(club[key], value)
            self.assertEqual(result, "edited club")

    def test_deleteClub(self):
        # Test if a club can be deleted
        with app.app_context():
            club_id = 1
            result, code = ClubService.delete_club(
                "test_student@columbia.edu", club_id)
            self.assertEqual(result, "club deleted")
            club = ClubService.get_club(club_id)
            self.assertIsNone(club)

    def test_invalid_deleteClub(self):
        # Test if a club can be deleted by anyone other than head
        with app.app_context():
            club_id = 1
            result, code = ClubService.delete_club(
                "test_student_2@columbia.edu", club_id)
            self.assertEqual(result, "Invalid Request")
            club = ClubService.get_club(club_id)
            self.assertIsNotNone(club)

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
            student_email = member_information["email_id"]
            student_id = StudentService.get_id(student_email)
            result, code = ClubService.add_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Club member added")
            role = Role.query.filter_by(student_id=student_id, club_id=club_id)
            self.assertEqual(role.first().role, "Club Member")

    def test_invalid_addClubMember(self):
        # Test if a club member can be added by anyone other than head
        with app.app_context():
            club_id = 1
            member_information = {
                "name": "TestMember",
                "email_id": "test_member@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            student_email = member_information["email_id"]
            StudentService.create_student(member_information)
            result, code = ClubService.add_member(
                "test_student_3@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Invalid Request")

    def test_invalid_addClubMember_3(self):
        # Test if a club member who is not a student can be added
        with app.app_context():
            club_id = 1
            result, code = ClubService.add_member(
                "test_student@columbia.edu", club_id,
                "test_member@columbia.edu")
            self.assertEqual(result, "error: student isn't registered")

    def test_removeClubMember(self):
        # Test if a club member can be removed
        with app.app_context():
            club_id = 1
            member_information = {
                "name": "TestMember",
                "email_id": "test_member@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(member_information)
            student_email = member_information["email_id"]
            result, code = ClubService.add_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Club member added")
            result, code = ClubService.remove_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Club member has been removed")

    def test_invalid_removeClubMember(self):
        # Test if a club member can be removed without authorization
        with app.app_context():
            club_id = 1
            member_information = {
                "name": "TestMember",
                "email_id": "test_member@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(member_information)
            student_email = member_information["email_id"]
            result, code = ClubService.add_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Club member added")
            result, code = ClubService.remove_member(
                None, club_id, student_email)
            self.assertEqual(result, "Invalid Request")

    def test_invalid_removeClubMember_2(self):
        # Test what happens if person who is not a member
        # is being removed
        with app.app_context():
            club_id = 1
            member_information = {
                "name": "TestMember",
                "email_id": "test_member@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(member_information)
            student_email = member_information["email_id"]
            result, code = ClubService.add_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Club member added")
            result, code = ClubService.remove_member(
                "test_student@columbia.edu", club_id,
                "test_member_2@columbia.edu")
            self.assertEqual(result, "error: student isn't registered")

    def test_invalid_removeClubMember_3(self):
        # Test what happens if a club member is being removed
        # from a club that doesn't exist
        with app.app_context():
            club_id = 1
            member_information = {
                "name": "TestMember",
                "email_id": "test_member@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(member_information)
            student_email = member_information["email_id"]
            result, code = ClubService.add_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "Club member added")
            club_id = 2
            result, code = ClubService.remove_member(
                "test_student@columbia.edu", club_id, student_email)
            self.assertEqual(result, "club does not exist")

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

    def test_assignSuccessor(self):
        # Test if a club head has been assigned
        with app.app_context():
            club_id = 1
            new_head_information = {
                "name": "TestHead",
                "email_id": "test_head@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(new_head_information)
            new_head_email_id = new_head_information["email_id"]
            result, code = ClubService.assign_successor(
                "test_student@columbia.edu", club_id, new_head_email_id)
            self.assertEqual(result, "replaced successor")

    def test_invalid_assignSuccessor(self):
        # Test if a club head who is not a student
        # can be assigned
        with app.app_context():
            club_id = 1
            new_head_email_id = "test_head_3@columbia.edu",
            result, code = ClubService.assign_successor(
                "test_student@columbia.edu", club_id, new_head_email_id)
            self.assertEqual(result, "error: student isn't registered")

    def test_invalid_assignSuccessor_2(self):
        # Test if a another than club head can
        #  assign a new head
        with app.app_context():
            club_id = 1
            new_head_information = {
                "name": "TestHead",
                "email_id": "test_head@columbia.edu",
                "college": "Fu Foundation",
                "department": "Computer Science"
            }
            StudentService.create_student(new_head_information)
            new_head_email_id = new_head_information["email_id"]
            result, code = ClubService.assign_successor(
                "test_student_3@columbia.edu", club_id, new_head_email_id)
            self.assertEqual(result, "Invalid Request")

    def tearDown(self):
        with app.app_context():
            db.drop_all()
            db.session.commit()


if __name__ == '__main__':
    unittest.main()
