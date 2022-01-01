import collections
import hashlib
import hmac
import re
import time
from urllib.parse import unquote, urljoin

import click
from flask import Blueprint, abort, current_app, make_response, redirect, request
from flask.cli import AppGroup
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_current_user,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from .login_session import new_login_session, find_session_by_name, abandon_session_invalid, terminate_session, is_session_expired
from .user import User

jwt = JWTManager()

def init_app(app):
    jwt.init_app(app)

@jwt.expired_token_loader
def clear_user_session(jwt_header, jwt_payload):
    _ = jwt_header
    try:
        _, session_name = jwt_payload['sub'].split('.')
        terminate_session(session_name)
    except:
        pass
    finally:
        return make_response({
            "error": "token has expired"
        }, 401)

@jwt.user_lookup_loader
def load_user_from_db(jwt_header, jwt_payload):
    _ = jwt_header
    user_id, session_name = jwt_payload['sub'].split('.')
    user = User.query.filter_by(id=user_id).first()
    if user is not None and is_session_expired(session_name) is False:
        return {
            "id": user.id,
            "tlg_username": user.telegram_username,
            "tlg_userid": user.telegram_userid
        }
    return None

bp = Blueprint('auth', __name__)
@bp.route("/auth/<string:session_name>", methods=("POST",))
def login(session_name):
    params = request.get_json()
    if params is None:
        return abort(401)

    otp = params['otp']
    if otp == None:
        return abort(401)

    lsession = find_session_by_name(session_name)
    if lsession == None or lsession.otp != otp:
        return abort(401)
    user = User.query.get(lsession.user_id)
    if user == None or 'pin' not in params or not check_password_hash(user.pin, params['pin']):
        return abort(401)
    lsession.activate()
    abandon_session_invalid(user.id)
    jwt_sub = "{user_id}.{session_name}".format(user_id=user.id, session_name=lsession.session_name)
    return make_response({
        "token": create_access_token(jwt_sub)
    })

@bp.route("/telegram-login")
def telegram_login():
    query_params = request.args.to_dict()
    hash_check = query_params.pop('hash')
    sortParams = collections.OrderedDict(sorted(query_params.items()))
    message = "\n".join(["{}={}".format(k, unquote(v)) for k, v in sortParams.items()])
    secret = hashlib.sha256(current_app.config.get('TELEGRAM_SECRET').encode('utf-8'))
    hash_message = hmac.new(secret.digest(), message.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    if hash_check != hash_message:
        return abort(401)
    user = User.find_by_telegram_account(query_params.get('id'))
    current_time = int(time.time())
    jwt_auth_time = int(query_params.get('auth_date') or 0)
    if (current_time - jwt_auth_time) > current_app.config['JWT_ACCESS_TOKEN_EXPIRES'] or user is None:
        return abort(401)
    
    user.session_alias = hash_check
    user.save()

    lsession = new_login_session(user.id)
    lsession.activate()
    jwt_sub = "{user_id}.{session_alias}".format(user_id=user.id, session_name=lsession.session_name)
    token = create_access_token(jwt_sub)
    redirect_url = urljoin(request.headers.get('REFERER'), 'oauth/{}'.format(token))
    return redirect(redirect_url)

@bp.route("/me")
@jwt_required()
def me():
    user = get_current_user()
    return make_response({"status": "ok", "data": user})

cli = AppGroup('auth')
@cli.command('register', with_appcontext=True)
@click.argument('username')
def cli_register_user(username):
    user = User.find_by_telegram_account(username)
    if user is None:
        print(f'\n!Err: {username} does not exit\n')
        return
    pin = ''
    while re.match(r'^\d{4}$', pin.strip()) is None:
        pin = input('Pin (4 digits): ')

    user.pin = generate_password_hash(pin)
    user.save()
    print(f'\nSuccess!\n')
    

@cli.command("new_login_session", with_appcontext=True)
@click.argument('username')
def cli_new_session(username):
    user = User.find_by_telegram_account(username)
    if user is None:
        print(f'\n!Err: {username} does not exit\n')
        return
    session = new_login_session(user.id)
    print(session)
