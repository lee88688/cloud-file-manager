import os
import json


_config = json.load('config.json')
_CURRENT_DIR = os.path.split(__file__)[0]


ARIA2_HOST = _config['aria2']['host']
ARIA2_PORT = _config['aria2']['port']
ARIA2_TOKEN = _config['aria2']['token']

REDIS_HOST = _config['redis']['host']
REDIS_PORT = _config['redis']['port']
REDIS_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)  # 'redis://localhost:6379'

SQLITE_URL = 'sqlite:///' + _CURRENT_DIR + os.sep + 'db.sqlite3'

SPLIT_SIZE = _config['split_size']

FILE_PATH = os.path.join(os.path.abspath(_CURRENT_DIR, os.path.pardir), '.files')
