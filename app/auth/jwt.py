from flask.helpers import make_response
from flask_jwt_extended import JWTManager

from app import user
from .login_session import terminate_session, is_session_expired

jwt = JWTManager()

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
    usr = user.find_by_id(user_id=user_id)
    if usr is not None and is_session_expired(session_name) is False:
        return {
            "id": usr.id,
            "tlg_username": usr.telegram_username,
            "tlg_userid": usr.telegram_userid
        }
    return None