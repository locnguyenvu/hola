from .jwt import jwt


def init_app(app):
    jwt.init_app(app)
