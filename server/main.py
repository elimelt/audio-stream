from aiohttp import web
import aiohttp_jinja2
import jinja2
import os
import logging
from server.routes import setup_routes
from server.config import Config

def create_app():
    app = web.Application()
    app['config'] = Config()

    # Set up logging
    logging.basicConfig(level=app['config'].LOGGING_LEVEL, format=app['config'].LOGGING_FORMAT)
    app['logger'] = logging.getLogger('audio-streaming')

    templates = os.path.join(app['config'].STATIC_ROOT, 'html')
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(templates))
    setup_routes(app)
    return app

