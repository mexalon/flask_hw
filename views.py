from app import app
from flask import jsonify, request
from schema import USER_CREATE, AD_CREATE
from validator import validate
from models import User, Advert


@app.route('/test', methods=['GET', ])
def test_me():
    return jsonify({'test_me': 'OK!'})


@app.route('/users', methods=['POST'])
@validate(USER_CREATE)
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User(username=username)
    user.set_password(password)
    user.add()
    return jsonify(user.to_dict())


@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    if users:
        return jsonify({'users': [u.to_dict for u in users]})
    else:
        return jsonify({'resp': 'user not found'})


@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    user = User.query.get(uid)
    if user:
        return jsonify(user.to_dict)
    else:
        return jsonify({'resp': 'user not found'})
