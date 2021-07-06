from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask(__name__)
app.config.from_mapping(SQLALCHEMY_DATABASE_URI=config.POSTGRE_URI)
sq = SQLAlchemy(app)

