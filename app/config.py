import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://flask_hw:flask_hw@127.0.0.1:5432/flask_hw')

SALT = 'ksfh@#$$5Kgfkорплапл*&^*&7fy374'

ADMIN = 'admin'
ADMIN_PASS = os.getenv('ADMIN_PASS', 'temp_pass')