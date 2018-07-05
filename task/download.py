import os
from cloudr.model import db_app, db, OfflineDownload
from .celery import app
from cloudr.utils.aria2 import Aria2
from cloudr.config import ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN


aria2 = Aria2(ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN)


def _addUri(id, uris):
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
def addUri(id, uris):
    with db_app.app_context():
        r = _addUri(id, uris)
    return r


def add_new_file(id):
    download_file = OfflineDownload.query.filter(OfflineDownload.id == id).first()
    userid = download_file.userid
    filename = download_file.filename
    uploaddate = download_file.time
    path = download_file.path
    # todo: find the file and calculate the md5.


def _refresh():
    downloads = OfflineDownload.query.filter(OfflineDownload.done == False).all()
    for d in downloads:
        r = aria2.tellStatus(d.gid)
        files = r['result']['files'][0]
        total_length = r['result']['totalLength']
        completed = int(float(files['completedLength']) / float(total_length) * 100)
        done = (completed == 100)
        if d.filename is None:
            path = files['path']
            filename = os.path.split(path)[-1]
        else:
            filename = None
        OfflineDownload.query.filter(OfflineDownload.id == d.id).update({
            'filename': filename,
            'completed': completed,
            'done': done
        })
        db.session.commit()
        # if done move the file into file dir, and insert a row into File
        if done:
            add_new_file(d.id)
