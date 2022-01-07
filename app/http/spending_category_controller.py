from flask import request, make_response
from flask_jwt_extended import jwt_required

import app.spending.category as spending_category

@jwt_required()
def index():
    if request.method == "GET":
        return make_response({
            "data": list(map(lambda e: {
                "id": e.id,
                "name": e.name,
                "display_name": e.display_name
            }, spending_category.find({})))
        })
    elif request.method == "POST":
        params = request.get_json()
        if params is None or "name" not in params:
            return make_response({
                "error": "Invalid data"
            }, 400)
        params.setdefault("display_name", None)
        category = spending_category.create(params["name"], display_name=params["display_name"])
        return make_response({
            "status": "ok",
            "data": {
                "name": category.name,
                "display_name": category.display_name
            }
        })

@jwt_required()
def edit(id):
    if request.method == "DELETE":
        if spending_category.delete(id):
            return make_response({
                "status": "ok"
            })
        else:
            return make_response({
                "error": "something went wrong"
            }, 500)
    if request.method == "PUT":
        if spending_category.edit(id, request.get_json()):
            return make_response({
                "status": "ok"
            })
        else:
            return make_response({
                "error": "something went wrong"
            }, 500)