import os

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://flask_hw:flask_hw@127.0.0.1:5432/flask_hw')

REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379')

SALT = os.getenv('SALT', 'ksfh@#$$5Kgfkорплапл*&^*&7fy374')

ADMIN = os.getenv('ADMIN', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'temp_pass')

DEV_EMAIL = os.getenv('DEV_EMAIL', 'typeyouremail@gmail.com')
DEV_PASS = os.getenv('DEV_PASS', 'typeyourepass')