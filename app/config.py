# POSTGRE_URI = 'postgresql://flask_hw:flask_hw@127.0.0.1:5432/flask_hw'
import os

POSTGRE_URI = os.getenv('POSTGRE_URI', 'postgresql://flask_hw:flask_hw@127.0.0.1:5432/flask_hw')
SALT = 'ksfh@#$$5Kgfkорплапл*&^*&7fy374'