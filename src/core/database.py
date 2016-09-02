__author__ = 'degibenz'
import os
from motor import motor_asyncio as ma

__all__ = ('DB',)

MONGODB_SERVER_HOST = os.getenv('MONGODB_SERVER_HOST', '127.0.0.1')
MONGODB_SERVER_PORT = os.getenv('MONGODB_SERVER_PORT', '27017')

try:
    MONGODB_DB_NAME = os.environ['MONGODB_DB_NAME']
except(KeyError,):
    MONGODB_DB_NAME = 'vote-for-number'


class DB(object):
    db = None

    def __init__(self, loop=None):
        self.db = ma.AsyncIOMotorClient(
            '%s:%s' % (MONGODB_SERVER_HOST, MONGODB_SERVER_PORT),
            io_loop=loop
        )['%s' % MONGODB_DB_NAME]
