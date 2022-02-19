from flask import make_response, request
from flask_jwt_extended import jwt_required

import app.spending.method as spending_method

@jwt_required()
def index():
    global spending_method
    if request.method == "POST":
        params = request.get_json()
        method = spending_method.create_spending_method(
            name = params.get("name"),
            type = params.get("type"),
            alias = params.get("alias")
        )
        return make_response({
            "status": "ok", 
            "data": {
                "id": method.id,
                "name": method.name,
                "type": method.type
            }
        })
    else:
        data = list(map(lambda e: {
            "id": e.id,
            "name": e.name,
            "type": e.type,
            "alias": e.alias
        }, spending_method.find({})))
        return make_response({"status": "ok", "data": data})