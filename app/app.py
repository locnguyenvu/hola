from flask import Flask, make_response
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'/*')
    app.config.from_object("config.Local")

    app.add_url_rule('/', endpoint='index')
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

        from .bot import disptacher
        disptacher.init()

        from . import auth
        auth.init_app(app)
        app.register_blueprint(auth.bp)
        app.cli.add_command(auth.cli)

        from . import user
        app.register_blueprint(user.bp)

        from . import spending
        app.register_blueprint(spending.bp)

        from . import chart
        app.register_blueprint(chart.bp)

        from .bot import webhook, cli
        app.register_blueprint(webhook.bp)
        app.cli.add_command(cli.cmd_bot_setup)


    return app
