from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from auth.models import User
from auth.schemas import UserSchema
from extensions import db

api = Blueprint('users', __name__)


@api.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.order_by(User.id.desc()).all()
    user_schema = UserSchema(many=True)
    count = len(users)
    return {'users': user_schema.dump(users), 'count': count}


@api.route('/update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    schema = UserSchema(partial=True)
    user = User.query.get_or_404(user_id)
    user = schema.load(request.json, instance=user)

    db.session.add(user)
    db.session.commit()

    return {'user': f'User {user.email} has been updated.'}


@api.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {'user': f'User {user.email} has been deleted.'}

