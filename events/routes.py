from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from events.models import Event
from events.schema import EventSchema
from extensions import db
from utils import pagination

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
    search_query = request.args.get('search')
    events_query = Event.query

    if search_query:
        events_query = events_query.filter(Event.event_name.ilike(f"%{search_query}%"))

    schema = EventSchema(many=True)
    events = pagination(events_query, schema)

    return events


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
