from flask import make_response
from flask_jwt_extended import jwt_required

from app.user import User


@jwt_required()
def index():
    data = list(map(lambda e: {
        "id": e.id,
        "telegram_username": e.telegram_username,
        "is_active": e.is_active
    }, User.query.all()))
    return make_response({
        "data": data
    })
