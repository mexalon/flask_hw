from datetime import datetime
from sqlalchemy.orm import relationship

import hashlib
from app import db
import config

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    adverts = relationship('Advert', backref='adverts')

    def __str__(self):
        return f'{self.id} <> {self.username}'

    def __repr__(self):
        return str(self)

    def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        self.password = hashlib.md5(raw_password.encode()).hexdigest()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as er:
            raise Exception(f'DB error: {er}')


class Advert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    created_at = db.Column(db.DateTime, default=datetime.now)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __str__(self):
        return f'{self.id} <> {self.title}'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'owner': self.owner,
        }

    def add(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as er:
            raise Exception(f'DB error: {er}')
