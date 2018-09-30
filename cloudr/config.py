import os
import json


_config = json.load('config.json')


ARIA2_HOST = _config['aria2']['host']
ARIA2_PORT = _config['aria2']['port']
ARIA2_TOKEN = _config['aria2']['token']

REDIS_HOST = _config['redis']['host']
REDIS_PORT = _config['redis']['port']
REDIS_URL = 'redis://{}:{}'.format(REDIS_HOST, REDIS_PORT)  # 'redis://localhost:6379'

SQLITE_URL = 'sqlite:///' + os.path.split(__file__)[0] + os.sep + 'db.sqlite3'

SPLIT_SIZE = _config['split_size']

FILE_PATH = r'G:\cloud-file-manager\.files'
