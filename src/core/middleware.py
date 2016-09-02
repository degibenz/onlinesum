__author__ = 'degibenz'

from functools import wraps

from aiohttp.web import json_response

from models import Session
from core.exceptions import *

__all__ = ('check_auth',)


def check_auth(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):

        token_in_header = request._request.__dict__.get('headers').get('x-token', None)

        if token_in_header:
            try:
                token = Session(token=token_in_header)

                request._request.client = await token.check_by_token()

                if not token:
                    raise ClientNotFoundViaToken
                else:
                    return await func(request, *args, **kwargs)

            except(Exception,) as error:
                return json_response({
                    'status': False,
                    'error': '{}'.format(error)
                })

        else:
            return json_response({
                'status': False,
                'error': 'need token in headers'
            })

    return wrapper
