from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from auth.models import User
from auth.schemas import UserSchema
from users.schema import AllUserSchema
from extensions import db
from utils import pagination

api = Blueprint('users', __name__)


@api.route('/', methods=['GET'])
def get_users():
    users = User.query
    user_schema = AllUserSchema(many=True)

    all_users = pagination(users, user_schema)

    return all_users


@api.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    user_schema = AllUserSchema()
    user = user_schema.dump(user)
    return user


@api.route('/update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    schema = UserSchema(partial=True)
    user = User.query.get_or_404(user_id)
    user = schema.load(request.json, instance=user)

    db.session.commit()

    return {'user': f'User {user.email} has been updated.'}


@api.route('/delete/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return {'user': f'User {user.email} has been deleted.'}
