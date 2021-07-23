from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import POSTGRE_URL

app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=POSTGRE_URL)
db = SQLAlchemy(app)
