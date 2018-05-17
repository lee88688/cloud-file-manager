from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    # files = db.relationship("file", backref="user")

    def __repr__(self):
        return "<({}) {}>".format(self.id, self.username)


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("user.id"))
    filename = db.Column(db.String(40), nullable=False)
    virtualpath = db.Column(db.Text, nullable=False)
    realpath = db.Column(db.Text, nullable=False)
    md5 = db.Column(db.String(40), nullable=False)