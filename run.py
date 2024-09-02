from server.main import create_app
from aiohttp import web
from aiohttp.web import Application
import ssl
import logging
import argparse
import pathlib

logger = logging.getLogger(__name__)


def parse_args():
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('--host', default='0.0.0.0')
    argument_parser.add_argument('--port', default=8080)
    argument_parser.add_argument('--ssl-cert', default='cert.pem')
    argument_parser.add_argument('--ssl-key', default='key.pem')
    args = argument_parser.parse_args()

    # check certfile and keyfile exist
    if not pathlib.Path(args.ssl_cert).exists():
        logger.error(f"Cert file {args.ssl_cert} does not exist")
        exit(1)
    if not pathlib.Path(args.ssl_key).exists():
        logger.error(f"Key file {args.ssl_key} does not exist")
        exit(1)

    # Check port is valid
    try:
        args.port = int(args.port)
        if args.port < 1 or args.port > 65535:
            raise ValueError
    except ValueError:
        logger.error(f"Port must be a positive integer")
        exit(1)

    return args

if __name__ == '__main__':
    args = parse_args()
    app = create_app()

    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=args.ssl_cert, keyfile=args.ssl_key)

    logger.info(f"Starting server on {args.host}:{args.port}")

    web.run_app(app, host=args.host, port=args.port, ssl_context=ssl_context)