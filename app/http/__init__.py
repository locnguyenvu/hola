from .blueprint import *

def init_app(app):
    app.register_blueprint(auth_routes)
    app.register_blueprint(chart_routes)
    app.register_blueprint(report_routes)
    app.register_blueprint(spending_category_routes)
    app.register_blueprint(spending_log_routes)
    app.register_blueprint(spending_method_routes)
    app.register_blueprint(spending_tag_routes)
    app.register_blueprint(user_routes)

