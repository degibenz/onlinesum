__author__ = 'degibenz'

import json

from datetime import datetime
from uuid import UUID, uuid4
from bson.objectid import ObjectId

from motor.motor_asyncio import AsyncIOMotorClient

from bson.json_util import dumps
from core.database import DB
from core.exceptions import ObjectNotFound

__all__ = ('Session', 'MathResults')


class Session(object):
    collection = 'sessions'

    pk = ObjectId
    selected_number = int
    token = UUID
    loop = None
    db = AsyncIOMotorClient

    result = None

    def __init__(self, pk=None, number=None, token=None):
        database = DB()
        self.db = database.db

        self.pk = pk
        self.selected_number = number
        self.token = token

    async def get(self, **kwargs) -> dict:
        q = {"_id": ObjectId(self.pk)} if self.pk else kwargs

        self.result = await self.objects.find_one(q)

        if not self.result:
            raise ObjectNotFound(cls_name=self.__class__.__name__)

        await self.db.close()
        return json.loads(dumps(self.result))

    async def save(self) -> str:
        self.token = uuid4()

        insert_data = {
            'token': "%s" % self.token,
            'create_at': datetime.now(),
            'selected_number': self.selected_number
        }

        self.pk = await self.objects.insert(insert_data)

        await self.db.close()
        return "%s" % self.token

    async def vote(self, number) -> dict:
        if number in range(0, 11):
            self.selected_number = number

            self.objects.update({'_id': self.pk}, {'$set': {'selected_number': number}})

            self.result = {
                'status': True,
            }
        else:
            self.result = {
                'status': False,
                'error': 'number not in range 0-10'
            }
        return self.result

    async def check_by_token(self) -> dict:
        return await self.objects.find_one({'token': "{}".format(self.token)})

    @property
    def objects(self):
        return self.db["%s" % self.collection]


class MathResults(object):
    db = None
    result = {}

    def __init__(self):
        database = DB()
        self.db = database.db['sessions']

    async def math_all_selected_number(self, future, websockets):
        cursor = await self.db.aggregate([{'$group': {'_id': None, 'sum': {'$sum': "$selected_number"}}}], cursor=False)

        self.result = {
            'sum': "%s" % cursor['result'][0].get('sum'),
            'websockets': websockets
        }

        future.set_result(self.result)
