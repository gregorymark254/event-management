from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from auth import User
from extensions import db
from auth.schemas import UserSchema

api = Blueprint('auth', __name__)


@api.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 400

    try:
        schema = UserSchema()
        user = schema.load(request.json)
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        return {"msg": str(err)}, 400

    return {"msg": f"User {user.email} Registered successfully"}, 201


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return {"msg": "Missing email or password"}, 400

    user = User.query.filter_by(email=email).first()
    if user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200
    else:
        return {'message': 'Incorrect password'}, 401
