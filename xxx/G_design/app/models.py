from .ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(16))
    passwd = db.Column(db.String(255))
