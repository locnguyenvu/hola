from . import blueprint

def init_app(app):
    app.register_blueprint(blueprint.auth)
    app.register_blueprint(blueprint.chart)
    app.register_blueprint(blueprint.spending_category)
    app.register_blueprint(blueprint.spending_log)
    app.register_blueprint(blueprint.spending_method)
    app.register_blueprint(blueprint.spending_tag)
    app.register_blueprint(blueprint.user)