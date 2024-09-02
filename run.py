from server.main import create_app
from aiohttp import web
from aiohttp.web import Application
import ssl
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = create_app()

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    logger.info(f"Starting server on {app['config'].HOST}:{app['config'].PORT} with SSL.")

    web.run_app(app, host='0.0.0.0', port=8080, ssl_context=ssl_context)