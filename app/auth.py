import re
import os
import click
import collections
import hashlib
import hmac
import time
from flask.cli import AppGroup
from base64 import b64encode
from flask import Blueprint, make_response, abort, request, current_app, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_current_user, jwt_required
from urllib.parse import urljoin, unquote
from .user import User

jwt = JWTManager()

def init_app(app):
    jwt.init_app(app)

@jwt.expired_token_loader
def clear_user_session(jwt_header, jwt_payload):
    try:
        sub = jwt_payload['sub']
        User.clear_session(sub)
    except:
        pass
    finally:
        return make_response({
            "error": "token has expired"
        }, 401)

@jwt.user_lookup_loader
def load_user_from_db(jwt_header, jwt_payload):
    sub = jwt_payload['sub']
    user = User.query.filter_by(telegram_userid=sub).first()
    if user is not None:
        return {
            "id": user.id,
            "tlg_username": user.telegram_username,
            "tlg_userid": user.telegram_userid
        }
    return user

bp = Blueprint('auth', __name__)

@bp.route("/login/<string:session_alias>", methods=("POST",))
def login(session_alias):
    params = request.get_json()
    user = User.query.filter_by(session_alias=session_alias).first()
    if user is None or params is None or 'pin' not in params or not check_password_hash(user.pin, params['pin']):
        return abort(401)
    return make_response({
        "token": create_access_token(user.session_alias)
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
    if (current_time - int(query_params.get('auth_date'))) > 86400 or user is None:
        return abort(401)
    
    user.session_alias = hash_check
    user.save()

    token = create_access_token(user.telegram_userid)
    redirect_url = urljoin(request.headers.get('REFERER'), 'oauth/{}'.format(token))
    print(redirect_url)
    return redirect(redirect_url)

@bp.route("/me")
@jwt_required()
def me():
    user = get_current_user()
    return make_response({"status": "ok", "data": user})

cli = AppGroup('auth')

@cli.command('register')
@click.argument('username')
def cli_register_user(username):
    user = User.find_by_telegram_account(username)
    if user is None:
        print(f'\n!Err: {username} does not exit\n')
        return
    pin = ''
    while re.match('^\d{4}$', pin.strip()) is None:
        pin = input('Pin (4 digits): ')

    user.pin = generate_password_hash(pin)
    user.save()
    print(f'\nSuccess!\n')
    