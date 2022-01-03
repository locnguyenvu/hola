from . import auth_command

def init_app(app):
    app.cli.add_command(auth_command.cli)