from flask import Blueprint, request
from marshmallow import ValidationError

from events import Attendance
from events.schema import AttendanceSchema
from extensions import db

api = Blueprint('attendance', __name__)


@api.route('/', methods=['POST'])
def create_attendance():
    schema = AttendanceSchema()
    attendance = schema.load(request.json)

    db.session.add(attendance)
    db.session.commit()

    return {'message': 'Attendance created'}, 201


@api.route('/', methods=['GET'])
def get_attendance():
    try:
        events = Attendance.query.all()
        schema = AttendanceSchema(many=True)
        count = len(events)
        return {'attendance': schema.dump(events), 'count': count}, 201
    except ValidationError as err:
        return err


@api.route('/<int:event_id>', methods=['GET'])
def get_attendance_by_event_id(event_id):
    try:
        event = Attendance.query.filter_by(event_id=event_id).all()
        schema = AttendanceSchema(many=True)
        count = len(event)
        return {'attendance': schema.dump(event), 'count': count}, 201
    except ValidationError as err:
        return err