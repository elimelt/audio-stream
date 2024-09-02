from audio_streaming.main import create_app
from aiohttp import web
from aiohttp.web import Application

if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host=app['config'].HOST, port=app['config'].PORT)