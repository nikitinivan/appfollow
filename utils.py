import json
import base64


class Serializer:
    """
    Class with static methods for safe saving list into MySQL database
    """

    @staticmethod
    def serialize(lst):
        """Return SQL-safe base64 format"""
        stringify = json.dumps(lst)
        serialized = base64.b64encode(stringify.encode('utf-8'))
        return serialized

    @staticmethod
    def deserialize(serialized):
        """Return list from base64"""
        deserialized = base64.b64decode(serialized)
        destringify = json.loads(deserialized.decode('utf-8'))
        return destringify
