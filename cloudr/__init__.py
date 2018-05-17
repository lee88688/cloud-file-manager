import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.split(__file__)[0] + os.sep + "db.sqlite3"
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    return app