import os
import click
from flask.cli import with_appcontext
from flask import Flask
from flask_login import LoginManager
from .model import db
from .config import FILE_PATH, SQLITE_URL


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from .model import Users
    return Users.get(int(user_id))


@click.command("init-db")
@with_appcontext
def init_db_command():
    from . import model
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Initialized the database.")


def init_file_type_table():
    from . import model
    for file_type in model.FileType.file_types:
        ft = model.FileType(filetype=file_type)
        db.session.add(ft)
    db.session.commit()
    click.echo("Initialized file_type table.")


@click.command("add-user")
@click.argument("name")
@click.argument("password")
@with_appcontext
def add_user(name, password):
    from .model import Users
    u = Users(username=name, password=password)
    db.session.add(u)
    db.session.commit()
    click.echo("add " + str(u) + " success.")


@click.command('init-table')
@with_appcontext
def init_table():
    init_file_type_table()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URL
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['FILE_PATH'] = FILE_PATH
    app.config['LOGIN_DISABLED'] = True

    db.init_app(app)
    login_manager.init_app(app)

    from . import api
    from . import file
    from . import views
    app.register_blueprint(api.bp)
    app.register_blueprint(file.bp)
    app.register_blueprint(views.app_bp)

    app.cli.add_command(init_db_command)
    app.cli.add_command(init_table)
    app.cli.add_command(add_user)

    return app
