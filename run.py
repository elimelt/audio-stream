from server.main import create_app
from aiohttp import web
from aiohttp.web import Application
import ssl

if __name__ == '__main__':
    app = create_app()

    # SSL context setup
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')

    # Start the app with SSL
    web.run_app(app, host='0.0.0.0', port=8080, ssl_context=ssl_context)