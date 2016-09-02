__author__ = 'degibenz'
import bson
import json
import datetime

__all__ = ('CustomEncoder',)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bson.objectid.ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
