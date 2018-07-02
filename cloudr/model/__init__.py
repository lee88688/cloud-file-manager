from flask import Flask
from ..config import SQLITE_URL
from .model import db, Users, File, FileType, OfflineDownload


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE_URL
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    return app


db_app = create_app()
