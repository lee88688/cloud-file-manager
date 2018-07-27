import os
import click
from flask.cli import with_appcontext
from flask import Flask, render_template
from flask_login import LoginManager
from .model import db
from .config import FILE_PATH, SQLITE_URL


login_manager = LoginManager()
login_manager.login_view = '/login'


@login_manager.user_loader
def load_user(user_id):
    from .model import Users
    return Users.query.filter(Users.id == int(user_id)).first()


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
    add_user('lee', '123')


def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = os.urandom(24)
    app.config['LOGIN_DISABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URL
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['FILE_PATH'] = FILE_PATH

    db.init_app(app)
    login_manager.init_app(app)

    from . import api
    from . import file
    from . import views
    app.register_blueprint(api.bp)
    app.register_blueprint(file.bp)
    app.register_blueprint(views.app_bp)
    app.register_blueprint(views.view_bp)

    app.cli.add_command(init_db_command)
    app.cli.add_command(init_table)

    return app
