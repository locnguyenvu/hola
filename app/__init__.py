from __future__ import absolute_import
from flask import Flask, make_response
from flask_cors import CORS
import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'/*')
    app.config.from_object("config.Local")

    @app.route('/health_check')
    def healthcheck():
        return {"status": "ok"}
    _ = healthcheck()

    def handle_client_error(error):
        return make_response({
            "error": f"{error}"
        }, 400)
    app.register_error_handler(400, handle_client_error)

    with app.app_context():
        from . import di
        di.bootstrap(app)

        from . import dbconfig
        dbconfig.load_dbconfig(app)

        from . import auth, http, cli
        auth.init_app(app)
        http.init_app(app)
        cli.init_app(app)

    return app


_ = create_app
