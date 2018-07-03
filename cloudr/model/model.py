from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return "<({}) {}>".format(self.id, self.username)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filetype = db.Column(db.Integer, db.ForeignKey("file_type.id"), nullable=False)
    filename = db.Column(db.String(40), nullable=False)
    filesize = db.Column(db.Integer)
    uploaddate = db.Column(db.DateTime, nullable=False)
    path = db.Column(db.Text, nullable=False)
    md5 = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return "<File ({name}) {path}>".format(name=self.filename, path=self.path)


class FileType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filetype = db.Column(db.String(10), nullable=False)

    file_types = ['directory', 'image', 'video', 'audio', 'document', 'zip', 'other']

    def __repr__(self):
        return '<({}) {}>'.format(self.id, self.filetype)


class OfflineDownload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(40))
    path = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    gid = db.Column(db.String(16))
    completed = db.Column(db.Integer, nullable=False)  # from 0 to 100 percent
    done = db.Column(db.Boolean, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    error = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<{} {} {}%>'.format(self.id, self.filename, self.completed)
