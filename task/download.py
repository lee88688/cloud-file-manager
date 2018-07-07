import os
from hashlib import md5
from cloudr.model import db_app, db, OfflineDownload, File, FileType
from .celery import app
from cloudr.utils.aria2 import Aria2
from cloudr.utils.filetype import check_file_type
from cloudr.config import ARIA2_HOST, ARIA2_PORT, ARIA2_TOKEN, MAX_READ_SIZE, FILE_PATH


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
        OfflineDownload.query.filter(
            OfflineDownload.id == id).update({'gid': gid})
    db.session.commit()

    return r


@app.task
def addUri(id, uris):
    with db_app.app_context():
        r = _addUri(id, uris)
    return r


def add_new_file(id):
    download_file = OfflineDownload.query.filter(
        OfflineDownload.id == id).first()
    userid = download_file.userid
    filename = download_file.filename
    uploaddate = download_file.time
    path = download_file.path
    filesize = os.path.getsize(path)
    # find the file and calculate the md5.
    with open(path, 'rb') as f:
        m = md5()
        r = f.read(MAX_READ_SIZE)
        m.update(r)
        while len(r) > 0:
            r = f.read(MAX_READ_SIZE)
            m.update(r)
        md5_str = m.hexdigest()
    filetype = FileType.query.filter(FileType.filetype == check_file_type(filename)).first()
    if not filetype:
        raise TypeError('can not specify filetype for {}'.format(filename))
    filetype = filename.id
    file = File(
        userid=userid,
        filetype=filetype,
        filename=filename,
        filesize=filesize,
        uploaddate=uploaddate,
        path=path,
        md5=md5_str
    )
    db.session.add(file)
    # move the file to destination dir
    new_path = FILE_PATH + os.sep + md5_str
    os.rename(path, new_path)


def _refresh():
    downloads = OfflineDownload.query.filter(
        OfflineDownload.done == False).all()
    for d in downloads:
        r = aria2.getFiles(d.gid)
        if 'error' in r:
            error_code = r['error']['code']
            error_message = r['error']['message']
            d.code = error_code
            d.message = error_message
            d.done = True
            db.session.commit()
            continue
        result = r['result'][0]
        total_length = r['result']['length']
        completed = int(
            float(result['completedLength']) / float(total_length) * 100)
        done = (completed == 100)
        path = result['path']
        if d.filename is None:
            filename = os.path.split(path)[-1]
        else:
            filename = None
        OfflineDownload.query.filter(OfflineDownload.id == d.id).update({
            'filename': filename,
            'path': path,
            'completed': completed,
            'done': done
        })
        # if done move the file into file dir, and insert a row into File
        if done:
            add_new_file(d.id)
        db.session.commit()


@app.task
def refresh():
    # todo: when some files download error, they need to be removed from aria2 and delete files.
    with db_app.app_context():
        _refresh()
