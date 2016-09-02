__author__ = 'degibenz'

import os
import asyncio

from aiohttp import web
from api import *

app_server = web.Application()

app_server.router.add_route('POST', '/session', JoinUser)
app_server.router.add_route('POST', '/vote', Vote)
app_server.router.add_route('GET', '/online', OnlineSum)
app_server['websockets'] = []

SERVER_PORT = int(os.getenv('SERVER_PORT', 8080))
SERVER_HOST = str(os.getenv('SERVER_HOST', '127.0.0.1'))

loop = asyncio.get_event_loop()


async def init(loop):
    srv = await loop.create_server(
        app_server.make_handler(),
        SERVER_HOST,
        SERVER_PORT
    )
    return srv


loop.run_until_complete(
    init(loop)
)

try:
    loop.run_forever()
except KeyboardInterrupt:
    loop.close()
