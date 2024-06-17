from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from events import Attendance
from events.schema import AttendanceSchema
from extensions import db
from utils import pagination

api = Blueprint('attendance', __name__)


@api.route('/', methods=['POST'])
@jwt_required()
def create_attendance():
    schema = AttendanceSchema()
    attendance = schema.load(request.json)

    db.session.add(attendance)
    db.session.commit()

    return {'message': 'Attendance created'}, 201


@api.route('/', methods=['GET'])
@jwt_required()
def get_attendance():
    attend = Attendance.query
    schema = AttendanceSchema(many=True)
    attendants = pagination(attend, schema)

    count = len(attendants)

    return {'attendance': attendants, 'count': count}, 201


@api.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_attendance_by_event_id(event_id):
    event = Attendance.query.filter_by(event_id=event_id)
    schema = AttendanceSchema(many=True)

    attendants = pagination(event, schema)
    count = len(attendants)

    return {'attendance': attendants, 'count': count}, 201
