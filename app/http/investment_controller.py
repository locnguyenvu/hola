from flask import request, make_response
from flask_jwt_extended import jwt_required

from app.investment import report

@jwt_required()
def index():
    return make_response({"message": "OK", "data": report.overview()})
