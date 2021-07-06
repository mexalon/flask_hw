from app import app
from flask import jsonify


@app.route('/test', methods=['GET', ])
def test_me():
    return jsonify({'test_me': 'OK!'})
