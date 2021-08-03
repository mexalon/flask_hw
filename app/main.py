from app import app
from aiohttp import web
import os


web.run_app(
    app,
    host='0.0.0.0',
    port=int(os.getenv('PORT', default=5000)),
)

