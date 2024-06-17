from flask import Flask, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from auth.routes import api
from events.routes import api as events_api
from users.routes import api as users_api
from attendance.routes import api as attendance_api
from extensions import migrate, db, jwt, cors

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
cors.init_app(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://eventsmanage.vercel.app"
    ]
}})


@app.route('/')
def hello_world():
    return 'Event Management Backend with flask'


# routes
app.register_blueprint(blueprint=api, url_prefix='/auth')
app.register_blueprint(blueprint=events_api, url_prefix='/events')
app.register_blueprint(blueprint=users_api, url_prefix='/users')
app.register_blueprint(blueprint=attendance_api, url_prefix='/attendance')


# handle errors in json format
@app.errorhandler(ValidationError)  # marshmallow validation errors
def validation_error(e):
    return jsonify(e.messages), 400


@app.errorhandler(SQLAlchemyError)  # sqlalchemy errors
def sqlalchemy_error(e):
    error_message = str(e)
    response = {
        'message': error_message,
    }
    return jsonify(response), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0')
