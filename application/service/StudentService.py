from app import db
from application.model.Student import Student

# Create new student entry
def create_student_db(student_information):

    name = student_information['name']
    email_id = student_information['email_id']
    college = student_information['college']
    department = student_information['department']

    new_student = Student(name=name, email_id=email_id, college=college, department=department)
    db.session.add(new_student)
    db.session.commit()

    return "Student Entry Created"
    
# Get information of a student using their email_id
def get_student_db(email_id=None):

    query = db.session.query(Student).filter(Student.email_id.in_([email_id]))
    results = query.all()
    return results


def get_id(email_id):

    student = db.session.query(Student).filter(Student.email_id.in_([email_id])).first()
    student_id = student._id
    return student_id

# {
#     "name": "TestStudent",
#     "email_id": "test_student@columbia.edu",
#     "college": "Fu Foundation",
#     "department": "Computer Science"
# }
