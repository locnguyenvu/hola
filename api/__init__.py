from flask import Flask, make_response

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Local")


    app.add_url_rule('/', endpoint='index')
    @app.route('/health_check')
    def healthcheck():
        return {"status": "ok"}

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

        from . import user
        app.register_blueprint(user.bp)

        from . import spending
        app.register_blueprint(spending.spending_log_bp)
        app.register_blueprint(spending.spending_category_bp)
        app.register_blueprint(spending.spending_method_bp)

    return app