from flask import Flask, make_response
from flask_cors import CORS

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
        from . import db, telebot
        db.init_app(app)
        telebot.init_app(app)

        from . import auth
        auth.init_app(app)

        from . import http, console, bot
        http.init_app(app)
        console.init_app(app)
        bot.init_app(app)

    return app
