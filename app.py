from flask import Flask
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
    "origins": ["http://127.0.0.1:3000"]
}})


@app.route('/')
def hello_world():
    return 'Event Management Backend with flask'


# routes
app.register_blueprint(blueprint=api, url_prefix='/auth')
app.register_blueprint(blueprint=events_api, url_prefix='/events')
app.register_blueprint(blueprint=users_api, url_prefix='/users')
app.register_blueprint(blueprint=attendance_api, url_prefix='/attendance')


if __name__ == '__main__':
    app.run()
