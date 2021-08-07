import jsonschema
from aiohttp import web
import hashlib
import config
from schema import USER_CREATE, AD_CREATE, EMAIL_SH
from models import User, Advert
from tasks import send_email


def check_admin_pass(password):
    some_password = f'{password}{config.SALT}'
    some_password = hashlib.md5(some_password.encode()).hexdigest()
    admin_password = f'{config.ADMIN_PASS}{config.SALT}'
    admin_password = hashlib.md5(admin_password.encode()).hexdigest()
    return admin_password == some_password


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
        return web.json_response({'test_me': f'OK! >> {config.REDIS_URL}'})


class SendEmailView:
    def __init__(self):
        pass

    async def get(self, request):
        return web.json_response({'ready': 'OK!'})

    async def get_task(self, request):
        """следит за статусом отправки по таск айди"""
        task_id = request.match_info['task_id']
        try:
            res = send_email.AsyncResult(task_id)
            return web.json_response({'status': f'{res.status}'})
        except Exception as er:
            print(f"fail >> {er}")

        return web.json_response({'status': 'fail'})

    async def send_to(self, request):
        """Шлёт письмо на указанный адрес"""
        header = request.headers
        username = header.get("username")
        password = header.get("password")
        if username == config.ADMIN and check_admin_pass(password):
            body = await request.json()
            body = await validate(body, EMAIL_SH)
            to = [body.get("email"), ]
            subject = body.get('subject', 'no subject')
            text = body.get('text')

            result = send_email.delay(subject, text, to)
            return web.json_response({'task_id': f'{result}'})

        else:
            return web.json_response({'resp': 'no auth'})

    async def send_to_all(self, request):
        """Шлёт рассылку по всем имеющимся адресам"""
        header = request.headers
        username = header.get("username")
        password = header.get("password")
        if username == config.ADMIN and check_admin_pass(password):
            body = await request.json()
            subject = body.get('subject', 'no subject')
            text = body.get('text')

            users = await User.query.gino.all()
            to = [u.email for u in users if u.email]
            result = send_email.delay(subject, text, to)

            return web.json_response({'task_id': f'{result}'})

        else:
            return web.json_response({'resp': 'no auth'})

    async def send_to_uid(self, request):
        """Шлёт письмо определённому пользователю"""
        header = request.headers
        username = header.get("username")
        password = header.get("password")
        if username == config.ADMIN and check_admin_pass(password):
            body = await request.json()
            subject = body.get('subject', 'no subject')
            text = body.get('text')
            user_id = request.match_info['uid']
            user = await User.get(int(user_id))
            if user:
                if user.email:
                    to = [user.email]
                    result = send_email.delay(subject, text, to)
                    return web.json_response({'task_id': f'{result}'})
                return web.json_response({'resp': 'no email'})
            else:
                return web.json_response({'resp': 'user not found'})

        else:
            return web.json_response({'resp': 'no auth'})


class UserView:
    def __init__(self):
        pass

    async def post(self, request):
        data = await request.json()

        data = await validate(data, USER_CREATE)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        try:
            user = await User.create(username=username, email=email)
            await user.set_password(password)
            return web.json_response(user.to_dict())

        except Exception as er:
            return web.json_response({'resp': f"cant create user {username}"})

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
        username = header.get("username")
        password = header.get("password")
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
        username = header.get("username")
        password = header.get("password")
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
