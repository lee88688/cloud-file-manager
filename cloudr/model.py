from . import db


class Users(db.Model):
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


class FileType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filetype = db.Column(db.String(10), nullable=False)

    file_types = ['directory', 'image', 'video', 'audio', 'document', 'zip', 'other']

    def __repr__(self):
        return '<({}) {}>'.format(self.id, self.filetype)


class OfflineDownload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
