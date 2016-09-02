__author__ = 'degibenz'

import asyncio
import traceback
from aiohttp.web import View, json_response, WebSocketResponse, web_logger

from models import Session, MathResults
from core.middleware import check_auth

__all__ = (
    'JoinUser', 'Vote', 'OnlineSum'
)


class OnlineSum(View):
    ws = None

    async def get(self):
        try:
            self.ws = WebSocketResponse()
            await self.ws.prepare(self.request)
            self.request.app['websockets'].append(self.ws)

            async for msg in self.ws:
                pass

        except(Exception,) as error:
            web_logger.error(error)
            traceback.print_exc()
            await self.ws.close()
        finally:
            return self.ws


class JoinUser(View):
    async def post(self):
        session = Session()
        response = {'status': True, 'session': await session.save()}
        return json_response(response)


class Vote(View):
    @check_auth
    async def post(self):
        data = await self.request.json()
        session = Session(pk=self.request.client.get('_id'))

        try:
            await session.vote(data.get('number'))
        except(Exception,) as error:
            web_logger.error(error)
            traceback.print_exc()

        try:
            future = asyncio.Future()
            math = MathResults()

            asyncio.ensure_future(math.math_all_selected_number(future, self.request.app['websockets']))

            future.add_done_callback(notify_to_sockets)

        except(Exception,) as error:
            web_logger.error(error)
            traceback.print_exc()

        return json_response(
            {'status': True}
        )


def notify_to_sockets(future):
    result = future.result()
    itog = result.get('sum')
    for socket in result.get('websockets'):
        future = asyncio.Future()
        asyncio.ensure_future(send_message(future, socket, itog))


async def send_message(future, socket, message):
    try:
        socket.send_str(data=message)
        future.set_result(True)
    except(Exception,):
        pass
