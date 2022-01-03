from . import webhook, cli

def init_app(app):
    app.register_blueprint(webhook.bp)
    app.cli.add_command(cli.cmd_bot_setup)