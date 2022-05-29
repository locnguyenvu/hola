from flask import request, make_response
from flask_jwt_extended import jwt_required

import app.spending.tag as spending_tag


@jwt_required()
def index():
    global spending_tag
    if request.method == 'GET':
        row_set = spending_tag.Tag.query.all()
        data = list(map(lambda e: {
            'id': e.id,
            'name': e.tag_name,
            'is_active': e.is_active
        }, row_set))
        return make_response({'status': 'ok', 'data': data})
    else:
        params = request.get_json()
        spending_tag = spending_tag.create_spending_tag(
            tag_name=params.get('tag_name')
        )
        return make_response({'status': 'ok', 'tag': {'tag_name': spending_tag.tag_name, 'id': spending_tag.id}})


@jwt_required()
def tag_log(tag_id):
    if request.method == 'POST':
        params = request.get_json()
        spending_tag.edit_spending_tag(tag_id, params)
        return make_response({'status': 'ok'})
    elif request.method == 'GET':
        tagged_logs = spending_tag.get_log_with_tag(tag_id)
        total = 0
        logs = []
        for log in tagged_logs:
            total += log.amount
            logs.append({
                "spending_log_id": log.id,
                "subject": log.subject,
                "amount": log.amount
            })
        return make_response({'total': total, 'logs': logs})
