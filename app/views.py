from flask import jsonify, request
from schema import USER_CREATE, AD_CREATE
from validator import validate
from models import User, Advert
from app import app, db


@app.route('/test', methods=['GET', ])
def test_me():
    return jsonify({'test_me': 'OK!'})


@app.route('/', methods=['GET', ])
def create_db():
    db.create_all()
    return jsonify({'db': 'OK!'})


@validate(USER_CREATE)
@app.route('/users', methods=['POST'])
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
        return jsonify({'users': [u.to_dict() for u in users]})
    else:
        return jsonify({'resp': 'users not found'})


@app.route('/users/<int:uid>', methods=['GET'])
def get_user(uid):
    user = User.query.get(uid)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({'resp': 'user not found'})


@app.route('/adverts', methods=['GET'])
def get_ads():
    ads = Advert.query.all()
    if ads:
        return jsonify({'adverts': [a.to_dict() for a in ads]})
    else:
        return jsonify({'resp': 'adverts not found'})


@app.route('/adverts/<int:uid>', methods=['GET'])
def get_ad(uid):
    ads = Advert.query.get(uid)
    if ads:
        return jsonify({'adverts': [a.to_dict() for a in ads]})
    else:
        return jsonify({'resp': 'advert not found'})


@validate(AD_CREATE)
@app.route('/adverts', methods=['POST'])
def new_ad():
    username = dict(request.headers).get("Username")
    password = dict(request.headers).get("Password")

    owner = User.query.filter(User.username == username).first()
    if owner:
        if owner.check_password(password):
            o_id = owner.id
            title = request.json.get('title')
            description = request.json.get('description')
            newad = Advert(title=title, description=description, owner=o_id)
            newad.add()
            return jsonify(newad.to_dict())

        return jsonify({'resp': 'wrong pass'})

    else:
        return jsonify({'resp': 'no auth'})


@validate(AD_CREATE)
@app.route('/adverts/<int:aid>', methods=['PATCH'])
def patch_ad(aid):
    ad = Advert.query.get(aid)
    if not ad:
        return jsonify({'resp': 'no such ad'})

    username = dict(request.headers).get("Username")
    password = dict(request.headers).get("Password")
    owner = User.query.filter(User.username == username).first()
    if owner:
        if owner.check_password(password):
            ad.title = request.json.get('title')
            ad.description = request.json.get('description')
            ad.add()

            return jsonify(ad.to_dict())

        return jsonify({'resp': 'wrong pass'})

    else:
        return jsonify({'resp': 'no auth'})


@app.route('/adverts/<int:aid>', methods=['DELETE'])
def del_ad(aid):
    ad = Advert.query.get(aid)
    if not ad:
        return jsonify({'resp': 'no such ad'})

    username = dict(request.headers).get("Username")
    password = dict(request.headers).get("Password")
    owner = User.query.filter(User.username == username).first()
    if owner:
        if owner.check_password(password):
            ad.delete()
            return jsonify({'resp': f'deleted'})

        return jsonify({'resp': 'wrong pass'})

    else:
        return jsonify({'resp': 'no auth'})
