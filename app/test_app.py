from app import app as tested_app
from models import User, Advert


async def test_get(aiohttp_client):
    client = await aiohttp_client(tested_app)
    r = await client.get('/test')
    assert r.status == 200
    assert await r.json() == {'test_me': 'OK!'}


async def test_post_u(aiohttp_client):
    client = await aiohttp_client(tested_app)
    test_user = {"username": "xhk382d47tri283c", "password": "testu12345serpassword"}
    r = await client.post('/users', json=test_user)
    assert r.status == 200
    data = await r.json()
    assert data.get("username") == test_user.get('username')
    uid = data.get('id')
    test_user = await User.get(int(uid))
    await test_user.delete()


async def test_post_a(aiohttp_client):
    client = await aiohttp_client(tested_app)
    test_user = {"username": "hfct56i3jrf7w4876i", "password": "testu12345serpassword"}
    test_ad = {"title": "test title", "description": "test descr"}

    u = await client.post('/users', json=test_user)
    assert u.status == 200
    data = await u.json()
    uid = data.get('id')

    r = await client.post('/adverts', headers=test_user, json=test_ad)
    assert r.status == 200
    data = await r.json()
    assert data.get("title") == test_ad.get('title')
    aid = data.get('id')

    temp_ad = await Advert.get(int(aid))
    await temp_ad.delete()

    temp_user = await User.get(int(uid))
    await temp_user.delete()
