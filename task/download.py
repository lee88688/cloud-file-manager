# from __future__ import absolute_import
from cloudr.model import db, OfflineDownload
from .celery import app
from cloudr.utils.aria2 import Aria2
from cloudr.config import ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN


aria2 = Aria2(ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN)


@app.task
def addUri(id, uris):
    if len(uris) > 1:
        raise TypeError("uris only support one uri.")
    r = aria2.addUri(uris)
    print(r)

    if 'error' in r:
        error_code = r['error']['code']
        error_message = r['error']['message']
        done = True
        OfflineDownload.query.filter(OfflineDownload.id == id).update({
            'error': error_code,
            'message': error_message,
            'done': done
        })
    else:
        gid = r['result']
        OfflineDownload.query.filter(OfflineDownload.id == id).update({'gid': gid})
    db.session.commit()

    return r


@app.task
def refresh():
    downloads = OfflineDownload.query.filter(OfflineDownload.done == False).all()
    for d in downloads:
        r = aria2.tellStatus(d.gid)
        files = r['result']['files'][0]
        total_length = r['result']['totalLength']
        completed = int(float(files['completedLength']) / float(total_length) * 100)
        done = (completed == 100)
        if d.filename is None:
            pass
