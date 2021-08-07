from aiohttp import web

from views import HealthView, UserView, AdvertView, SendEmailView
from models import db
from config import DATABASE_URL

CORRECT_DB_URL = DATABASE_URL
if CORRECT_DB_URL.startswith("postgres://"):
    CORRECT_DB_URL = CORRECT_DB_URL.replace("postgres://", "postgresql://", 1)


async def init_orm(app):
    await db.set_bind(CORRECT_DB_URL)
   # await db.gino.drop_all()
    await db.gino.create_all()
    yield
    await db.pop_bind().close()

app = web.Application()
app.cleanup_ctx.append(init_orm)

app.add_routes([web.get('/test', HealthView)])

user_view = UserView()
app.add_routes([
    web.get('/users', user_view.get),
    web.post('/users', user_view.post),
    web.get('/users/{uid:\d+}', user_view.get_user),
])

ad_view = AdvertView()
app.add_routes([
    web.get('/adverts', ad_view.get_ads),
    web.get('/adverts/{aid:\d+}', ad_view.get_ad),
    web.post('/adverts', ad_view.new_ad),
    web.patch('/adverts/{aid:\d+}', ad_view.patch_ad),
    web.delete('/adverts/{aid:\d+}', ad_view.del_ad),
])

send_email_view = SendEmailView()
app.add_routes([
    web.get('/send_to', send_email_view.get),
    web.post('/send_to_email', send_email_view.send_to),
    web.get('/send_to/{task_id}', send_email_view.get_task),
    web.post('/send_to_db', send_email_view.send_to_all),
    web.post('/send_to_db/{uid:\d+}', send_email_view.send_to_uid),
    ])
