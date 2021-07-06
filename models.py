from datetime import datetime

import config
from app import sq
from sqlalchemy.orm import relationship
import hashlib


class User(sq.Model):
    id = sq.Column(sq.Integer, primary_key=True)
    username = sq.Column(sq.String(50), unique=True)
    password = sq.Column(sq.String(50))
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


class Advert(sq.Model):
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(300))
    description = sq.Column(sq.String(3000))
    created_at = sq.Column(sq.DateTime, default=datetime.now)
    owner = sq.Column(sq.Integer, sq.ForeignKey('user.id'))

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
