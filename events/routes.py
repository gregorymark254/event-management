from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from marshmallow.exceptions import ValidationError

from events.models import Event
from events.schema import EventSchema
from extensions import db

api = Blueprint('events', __name__)


@api.route('/', methods=['POST'])
@jwt_required()
def add_events():
    schema = EventSchema()
    events = schema.load(request.json)

    db.session.add(events)
    db.session.commit()

    return {'events': f'Event {events.event_name} added successfully.'}, 201


@api.route('/', methods=['GET'])
@jwt_required()
def get_events():
    try:
        events = Event.query.all()
        schema = EventSchema(many=True)
        count = len(events)
        return {'events': schema.dump(events), 'count': count}, 201
    except ValidationError as err:
        return err


@api.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event_by_id(event_id):
    event = Event.query.get(event_id)
    schema = EventSchema()
    event = schema.dump(event)
    return {'event': event}, 201


@api.route('/update/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    schema = EventSchema(partial=True)
    event = Event.query.get(event_id)
    event = schema.load(request.json, instance=event)

    db.session.add(event)
    db.session.commit()
    return {'event': f'Event {event.event_name} updated successfully.'}, 201


@api.route('/delete/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return {'event': f'Event {event.event_name} deleted successfully.'}, 201
