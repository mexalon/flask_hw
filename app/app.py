from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL

app = Flask(__name__)

uri = DATABASE_URL
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config.from_mapping(SQLALCHEMY_DATABASE_URI=uri)
db = SQLAlchemy(app)
