from aiohttp import web
import aiohttp_jinja2
import jinja2
import os
from server.routes import setup_routes
from server.config import Config

def create_app():
    app = web.Application()
    app['config'] = Config()
    templates = os.path.join(app['config'].STATIC_ROOT, 'html')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates))
    setup_routes(app)
    return app