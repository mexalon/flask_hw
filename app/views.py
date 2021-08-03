import jsonschema
from aiohttp import web

from schema import USER_CREATE, AD_CREATE

from models import User, Advert


async def validate(data, req_schema):
    try:
        jsonschema.validate(
            data, schema=req_schema,
        )
    except jsonschema.ValidationError as er:
        print(er.message)
        raise web.HTTPBadRequest
    return data


class HealthView(web.View):
    async def get(self):
        return web.json_response({'test_me': 'OK!'})


class UserView:
    def __init__(self):
        pass

    async def post(self, request):
        data = await request.json()

        data = await validate(data, USER_CREATE)
        username = data.get('username')
        password = data.get('password')
        try:
            user = await User.create(username=username)
            await user.set_password(password)
            return web.json_response(user.to_dict())

        except Exception as er:
            print(er)
            raise web.HTTPBadRequest

    async def get(self, request):
        users = await User.query.gino.all()

        if users:
            return web.json_response({'users': [u.to_dict() for u in users]})
        else:
            return web.json_response({'resp': 'users not found'})

    async def get_user(self, request):
        user_id = request.match_info['uid']
        user = await User.get(int(user_id))
        if user:
            return web.json_response(user.to_dict())
        else:
            return web.json_response({'resp': 'user not found'})


class AdvertView:
    def __init__(self):
        pass

    async def get_ads(self, request):
        ads = await Advert.query.gino.all()
        if ads:
            return web.json_response({'adverts': [a.to_dict() for a in ads]})
        else:
            return web.json_response({'resp': 'adverts not found'})

    async def get_ad(self, request):
        ads_id = request.match_info['aid']
        ads = await Advert.get(int(ads_id))
        if ads:
            return web.json_response({'adverts': ads.to_dict()})
        else:
            return web.json_response({'resp': 'advert not found'})

    async def new_ad(self, request):
        header = request.headers
        username = header.get("Username")
        password = header.get("Password")
        owner = await User.query.where(User.username == username).gino.first()
        if owner:
            if owner.check_password(password):
                o_id = owner.id
                body = await request.json()
                body = await validate(body, AD_CREATE)
                title = body.get('title')
                description = body.get('description')
                newad = await Advert.create(title=title, description=description, owner=o_id)
                return web.json_response(newad.to_dict())

            return web.json_response({'resp': 'wrong pass'})

        else:
            return web.json_response({'resp': 'no auth'})

    async def patch_ad(self, request):
        ads_id = request.match_info['aid']
        ad = await Advert.get(int(ads_id))
        if not ad:
            return web.json_response({'resp': 'no such ad'})

        header = request.headers
        username = header.get("Username")
        password = header.get("Password")
        owner = await User.query.where(User.username == username).gino.first()
        if owner:
            if owner.check_password(password):
                body = await request.json()
                body = await validate(body, AD_CREATE)
                title = body.get('title')
                description = body.get('description')
                await ad.update(title=title, description=description).apply()

                return web.json_response(ad.to_dict())

            return web.json_response({'resp': 'wrong pass'})

        else:
            return web.json_response({'resp': 'no auth'})

    async def del_ad(self, request):
        ads_id = request.match_info['aid']
        ad = await Advert.get(int(ads_id))
        if not ad:
            return web.json_response({'resp': 'no such ad'})

        header = request.headers
        username = header.get("Username")
        password = header.get("Password")
        owner = await User.query.where(User.username == username).gino.first()
        if owner:
            if owner.check_password(password):
                await ad.delete()
                return web.json_response({'resp': f'deleted'})

            return web.json_response({'resp': 'wrong pass'})

        else:
            return web.json_response({'resp': 'no auth'})
