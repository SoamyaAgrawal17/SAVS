from app import db
from application.model import Student

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
    
def get_student_db(student_id=None):

    students = db.session.query(Student).filter_by(name='soamya')
    

    # students = Student.query.all()
    # students = Student.quer
    return students