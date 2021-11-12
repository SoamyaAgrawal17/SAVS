from application.controller.controllers import app
from application.controller.controllers import db

from application.model.Club import Club
from application.model.Events import Events
from application.model.Role import Role
from application.model.StudentEvents import StudentEvents
from application.model.Students import Students

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)