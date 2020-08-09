from .extensions import db

from datetime import datetime, timedelta
import secrets

class Key(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    starting_date = db.Column(db.DateTime, default=datetime.utcnow)
    expiration_date = db.Column(db.DateTime, default=datetime.utcnow() + timedelta(days=1))

    key_string = db.Column(db.String(150))

    def __init__(self, days=0, hours=0):
        if days == 0:
            hours = 1

        self.starting_date = datetime.utcnow()
        self.expiration_date = self.starting_date + \
            timedelta(days=days) + timedelta(hours=hours)
        self.key_string = secrets.token_hex(24)