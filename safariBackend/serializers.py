import json, asyncio
from base64 import b64decode, b64encode

class BytesJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return {'__class__': 'bytes', '__value__': b64encode(o).decode('ascii')}
        elif asyncio.iscoroutine(o):
            return None 
        return super().default(o)


class BytesJSONDecoder(json.JSONDecoder):
    def decode(self, s):
        def object_hook(o):
            if '__class__' in o and o['__class__'] == 'bytes':
                return b64decode(o['__value__'].encode('ascii'))
            return o
        return json.loads(s, object_hook=object_hook)