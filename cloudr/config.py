import os


ARIA2_HOST = 'localhost'
ARIA2_PORT = 6800
ARIA2_TOKEN = None

REDIS_URL = 'redis://localhost:6379'

SQLITE_URL = 'sqlite:///' + os.path.split(__file__)[0] + os.sep + 'db.sqlite3'

MAX_READ_SIZE = 1024 * 1024

FILE_PATH = r'G:\cloud-file-manager\.files'
