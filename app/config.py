# POSTGRE_URI = 'postgresql://flask_hw:flask_hw@127.0.0.1:5432/flask_hw'
import os

DATABASE_URL = os.getenv(
    'POSTGRE_URL',
    'postgresql://flask_hw:flask_hw@127.0.0.1:5432/flask_hw')
SALT = 'ksfh@#$$5Kgfkорплапл*&^*&7fy374'
