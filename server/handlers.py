import logging
from aiohttp import web
import aiohttp
import aiohttp_jinja2
from collections import defaultdict

logger = logging.getLogger(__name__)

channels = defaultdict(list)
channel_consumers = defaultdict(set)

@aiohttp_jinja2.template('index.html')
async def index(request):
    channel_id = request.match_info['channel_id']
    logger.info(f"Serving index page for channel {channel_id}")
    return {'channel_id': channel_id}

async def consume(request):
    channel_id = request.match_info['channel_id']
    ip = request.remote
    logger.info(f"New consumer connected to channel {channel_id} from {ip}")
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    channel_consumers[channel_id].add(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.ERROR:
                logger.error(f'WebSocket connection closed with exception {ws.exception()} from {ip}')
    finally:
        channel_consumers[channel_id].remove(ws)
        logger.info(f"Consumer disconnected from channel {channel_id} from {ip}")
    return ws

async def produce(request):
    channel_id = request.match_info['channel_id']
    ip = request.remote
    logger.info(f"New producer connected to channel {channel_id} from {ip}")
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                logger.info(f"Received binary message on channel {channel_id} from {ip}")
                channels[channel_id].append(msg.data)
                for consumer in channel_consumers[channel_id]:
                    await consumer.send_bytes(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                logger.error(f'WebSocket connection closed with exception {ws.exception()} from {ip}')
    finally:
        logger.info(f"Producer disconnected from channel {channel_id} from {ip}")
    return ws


async def get_metrics(request):
    metrics = {
        "total_channels": len(channels),
        "total_consumers": sum(len(consumers) for consumers in channel_consumers.values()),
        "channels": {
            channel_id: {
                "consumer_count": len(channel_consumers[channel_id]),
                "message_count": len(channels[channel_id])
            }
            for channel_id in channels
        }
    }
    logger.info("Metrics requested")
    return web.json_response(metrics)
