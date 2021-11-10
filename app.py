from application.controller.controllers import app
from application.controller.controllers import db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)