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

    from . import exceptions
    @app.errorhandler(exceptions.ClientException)
    def handle_client_error(error):
        return make_response({
            "error": f"{error}"
        }, 400)

    with app.app_context():
        from . import db
        db.init_app(app)

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

    return app
