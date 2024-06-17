import enum
from functools import wraps

import bcrypt
from datetime import datetime

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from extensions import db


class UserRoles(enum.Enum):
    admin = 'admin'
    user = 'user'


class User(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum(UserRoles), nullable=False)
    _password = db.Column("password", db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        hashed_password = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        self._password = hashed_password.decode('utf-8')

    def check_password(self, value):
        return bcrypt.checkpw(value.encode('utf-8'), self._password.encode('utf-8'))


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        if 'role' not in current_user or current_user['role'] != UserRoles.admin.value:
            return {'error': 'Unauthorized! Admin Only'}, 403

        return fn(*args, **kwargs)

    return wrapper
