__all__ = (
    'ObjectNotFound', 'TokeInHeadersNotFound',
    'TokenIsNotFound', 'ClientNotFoundViaToken'
)


class ObjectNotFound(Exception):
    cls_name = None

    def __init__(self, cls_name):
        self.cls_name = cls_name

    def __str__(self):
        return "Object :: {} not found".format(self.cls_name)


class TokeInHeadersNotFound(Exception):
    def __str__(self):
        return "requires authorization key in request-header"


class TokenIsNotFound(Exception):
    def __str__(self):
        return "token not found"


class ClientNotFoundViaToken(Exception):
    def __str__(self):
        return "Can't found client via token"
