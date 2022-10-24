import collections
import hashlib
import hmac
import time

from flask import make_response, abort, redirect, request, current_app
from flask_jwt_extended import create_access_token, get_current_user, jwt_required
from urllib.parse import unquote, urljoin
from werkzeug.security import check_password_hash

from app.auth import login_session
from app.user import User, find_by_telegram_account


def login(session_name):
    params = request.get_json()
    if params is None:
        return abort(401)

    otp = params['otp']
    if otp is None:
        return abort(401)

    lsession = login_session.find_session_by_name(session_name)
    if lsession is None or lsession.otp != otp:
        return abort(401)
    user = User.query.get(lsession.user_id)
    if user is None or 'pin' not in params or not check_password_hash(user.pin, params['pin']):
        return abort(401)
    lsession.activate(params.get("browser_info"))
    login_session.save(lsession)
    login_session.abandon_session_invalid(user.id)
    jwt_sub = "{user_id}.{session_name}".format(user_id=user.id, session_name=lsession.session_name)
    return make_response({
        "token": create_access_token(jwt_sub)
    })


def telegram_login():
    query_params = request.args.to_dict()
    hash_check = query_params.pop('hash')
    sortParams = collections.OrderedDict(sorted(query_params.items()))
    message = "\n".join(["{}={}".format(k, unquote(v)) for k, v in sortParams.items()])
    secret = hashlib.sha256(current_app.config.get('TELEGRAM_SECRET').encode('utf-8'))
    hash_message = hmac.new(secret.digest(), message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    if hash_check != hash_message:
        return abort(401)
    user = find_by_telegram_account(query_params.get('id'))
    current_time = int(time.time())
    jwt_auth_time = int(query_params.get('auth_date') or 0)
    if (current_time - jwt_auth_time) > current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] or user is None:
        return abort(401)

    user.session_alias = hash_check
    user.save()

    lsession = login_session.new_login_session(user.id)
    lsession.activate("Telegram internal browser")
    login_session.save(lsession)
    jwt_sub = "{user_id}.{session_name}".format(user_id=user.id, session_name=lsession.session_name)
    token = create_access_token(jwt_sub)
    redirect_url = urljoin(request.headers.get('REFERER'), 'oauth/{}'.format(token))
    return redirect(redirect_url)


@jwt_required()
def me():
    user = get_current_user()
    return make_response({"status": "ok", "data": user})
