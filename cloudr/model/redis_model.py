import json
import os
from walrus import Model, Walrus, IntegerField, ListField, TextField, DateTimeField


_config = json.load(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json'))
redis_db = Walrus(host=_config['redis']['host'], port=_config['redis']['port'], db=0)


class UploadCache(Model):
    __database__ = redis_db

    _id = 0
    id = IntegerField(primary_key=True)
    cache = ListField()
    sequence_number = IntegerField(default=0)
    max_sequence_number = IntegerField(default=0)
    # store upload file information
    size = IntegerField(default=0)
    path = TextField(default='/')
    md5 = TextField()
    upload_date = DateTimeField()
    file_name = TextField()
    filetype = IntegerField()
    user_id = IntegerField()

    @classmethod
    def generate_id(cls):
        rv = cls._id
        cls._id += 1
        return rv
