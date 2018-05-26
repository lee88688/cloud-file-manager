import os
import click
from flask.cli import with_appcontext
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


@click.command("init-db")
@with_appcontext
def init_db_command():
    from . import model
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Initialized the database.")


@click.command("init-file-type")
@with_appcontext
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


def create_app():
    app = Flask(__name__, static_folder="static")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.split(__file__)[0] + os.sep + "db.sqlite3"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['FILE_PATH'] = r'G:\cloud-file-manager\.files'

    db.init_app(app)

    from . import api, file
    app.register_blueprint(api.bp)
    app.register_blueprint(file.bp)
    
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_file_type_table)
    app.cli.add_command(add_user)

    return app