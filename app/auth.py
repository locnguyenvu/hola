import re
import os
import click
from flask.cli import AppGroup
from base64 import b64encode
from flask import Blueprint, make_response, abort, request, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, get_current_user, jwt_required
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
    user = User.query.filter_by(session_alias=sub).first()
    if user is not None:
        return {
            "id": user.id,
            "tlg_username": user.telegram_username,
            "tlg_userid": user.telegram_userid
        }
    return user

bp = Blueprint('auth', __name__)

@bp.route("/lmi/<string:telegram_account_identity>")
def logmein(telegram_account_identity):
    user = User.find_by_telegram_account(telegram_account_identity)
    if user is None:
        return abort(401)
    
    user.session_alias = re.sub("[\/=]", "", b64encode(os.urandom(10)).decode("utf8"))
    user.save()
    return make_response({
        "session_id": user.session_alias
    })

@bp.route("/login/<string:session_alias>", methods=("POST",))
def login(session_alias):
    params = request.get_json()
    user = User.query.filter_by(session_alias=session_alias).first()
    if user is None or params is None or 'pin' not in params or not check_password_hash(user.pin, params['pin']):
        return abort(401)
    return make_response({
        "token": create_access_token(user.session_alias)
    })

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
    