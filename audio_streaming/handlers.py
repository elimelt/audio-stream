import aiohttp
from aiohttp import web
import jinja2
import aiohttp_jinja2
from collections import defaultdict

channels = defaultdict(list)
channel_consumers = defaultdict(set)

@aiohttp_jinja2.template('index.html')
async def index(request):
    channel_id = request.match_info['channel_id']
    return {'channel_id': channel_id}

async def consume(request):
    channel_id = request.match_info['channel_id']
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    channel_consumers[channel_id].add(ws)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {ws.exception()}')
    finally:
        channel_consumers[channel_id].remove(ws)
    return ws

async def produce(request):
    channel_id = request.match_info['channel_id']
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                channels[channel_id].append(msg.data)
                for consumer in channel_consumers[channel_id]:
                    await consumer.send_bytes(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print(f'WebSocket connection closed with exception {ws.exception()}')
    finally:
        pass
    return ws