from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URL

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=DATABASE_URL)
db = SQLAlchemy(app)
