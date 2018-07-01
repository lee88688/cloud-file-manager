# from __future__ import absolute_import
from cloudr import create_app
from cloudr.model import db
from .celery import app
from cloudr.utils.aria2 import Aria2
from cloudr.config import ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN


flask_app = create_app()
aria2 = Aria2(ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN)


@app.task
def addUri(uris):
    if len(uris) > 1:
        raise TypeError("uris only support one uri.")
    r = aria2.addUri(uris)
    print(r)
    return r
