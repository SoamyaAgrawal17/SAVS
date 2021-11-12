
from application.controller.controllers import app
from application.controller.controllers import db

from application.model.Club import Club
from application.model.Event import Event
from application.model.Role import Role
from application.model.StudentEvent import StudentEvent
from application.model.Student import Student

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)