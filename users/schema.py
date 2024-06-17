from marshmallow.fields import Function
from extensions import ma
from auth import User


class AllUserSchema(ma.SQLAlchemyAutoSchema):
    role = Function(lambda obj: obj.role.value)

    class Meta:
        model = User
        load_instance = True
