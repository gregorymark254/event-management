from marshmallow import validate, validates_schema, ValidationError
from marshmallow.validate import Email

from extensions import ma
from marshmallow.fields import String

from events.models import Attendance, Event


class EventSchema(ma.SQLAlchemyAutoSchema):
    event_name = String(required=True, validate=validate.Length(min=5))

    @validates_schema
    def validate_event_name(self, data, **kwargs):
        event_name = data.get("event_name")
        if Event.query.filter_by(event_name=event_name).count():
            raise ValidationError(f'Event {event_name} is already registered')

    class Meta:
        model = Event
        load_instance = True


class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    email = String(required=True, validate=Email())
    phone = String(required=True, validate=validate.Length(max=10, error='Phone number must be number'))

    @validates_schema
    def validate_phone(self, data, **kwargs):
        phone = data.get("phone")
        if Attendance.query.filter_by(phone=phone).count():
            raise ValidationError('Phone already exist')

    class Meta:
        model = Attendance
        load_instance = True
        include_fk = True
