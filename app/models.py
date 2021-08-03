from gino import Gino
from datetime import datetime
import hashlib
import config

db = Gino()


class User(db.Model):
    __tablename__ = 'app_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    def __str__(self):
        return f'{self.id} <> {self.username}'

    def __repr__(self):
        return str(self)

    async def set_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        await self.update(password=hashlib.md5(raw_password.encode()).hexdigest()).apply()

    def check_password(self, raw_password: str):
        raw_password = f'{raw_password}{config.SALT}'
        return self.password == hashlib.md5(raw_password.encode()).hexdigest()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }


class Advert(db.Model):
    __tablename__ = 'app_adverts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300))
    description = db.Column(db.String(3000))
    created_at = db.Column(db.DateTime, default=datetime.now)
    owner = db.Column(db.Integer, db.ForeignKey('app_users.id'))

    def __str__(self):
        return f'{self.id} <> {self.title}'

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'owner': self.owner,
        }

