import os
import hashlib
from datetime import datetime
from flask import jsonify, request, current_app
from cloudr.model import File, Users, FileType, OfflineDownload, db
from . import bp
from task.download import addUri
from cloudr.utils import change_path_prefix
from flask_login import login_required, current_user


@bp.route("/hello", methods=["GET", "POST"])
def hello():
    return jsonify(greet="hello")


@bp.route("/get-path-content", methods=["POST"])
@login_required
def get_path_content():
    user_name = current_user.username
    path = request.json['path']
    files = File.query.join(Users).join(FileType).\
                       filter(Users.username == user_name, File.path == path).\
                       add_columns(FileType.filetype).all()

    rv = {"result": "success", "files": []}
    for index, f in enumerate(files):
        file_item = {}
        file_item['id'] = index
        file_item['fileName'] = f.File.filename
        file_item['fileType'] = f.filetype
        file_item['fileSize'] = f.File.filesize
        file_item['modifiedTime'] = f.File.uploaddate.strftime("%Y-%m-%d %H:%M:%S")
        file_item['path'] = f.File.path
        rv['files'].append(file_item)

    return jsonify(rv)


@bp.route("/delete-resource", methods=["POST"])
@login_required
def delete_resource():
    dir_file_type = FileType.query.filter(FileType.filetype == 'directory').first().id
    user_name = current_user.username
    path = request.json['path']  # todo: path check
    file_list = request.json["fileList"]
    for file_name in file_list:
        file = File.query.join(Users).join(FileType).\
                        filter(Users.username == user_name).\
                        filter(File.path == path).\
                        filter(File.filename == file_name).first()
        if file:
            if file.filetype != dir_file_type:
                real_file_name = current_app.config["FILE_PATH"] + os.sep + file.md5
                File.query.filter(File.id == file.id).delete()
                if os.path.isfile(real_file_name):
                    os.remove(real_file_name)
            else:
                # todo: delete the whole directory
                File.query.filter(File.id == file.id).delete()
        else:
            pass
    db.session.commit()
    return jsonify({"result": "success"})


@bp.route("/new-directory", methods=["POST"])
@login_required
def new_directory():
    user_name = current_user.username
    size = 0
    path = request.json['path']  # todo: path check
    md5 = "-"
    upload_date = datetime.now()
    # file_name = secure_filename(request.json['dirName'])
    file_name = request.json['dirName']  # todo: check file name to void repeat
    file_type = FileType.query.filter(FileType.filetype == 'directory').first().id
    user_id = Users.query.filter(Users.username == user_name).first().id  # todo: catch user_name is not found

    file = File(userid=user_id, filetype=file_type, filename=file_name, filesize=size, uploaddate=upload_date, path=path, md5=md5)
    db.session.add(file)
    db.session.commit()

    file_info = {}
    file_info["id"] = file.id
    file_info["fileName"] = file.filename
    file_info["fileType"] = "directory"
    file_info["fileSize"] = file.filesize
    file_info["modifiedTime"] = file.uploaddate.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({"result": "success", "file": file_info})


@bp.route("/rename-resource", methods=["POST"])
@login_required
def rename_resource():
    new_name = secure_filename(request.json['newname'])
    old_name = request.json['oldname']
    path = request.json['path']
    user_name = current_user.username

    file = File.query.join(Users).filter(Users.username == user_name,
                                       File.path == path,
                                       File.filename == old_name).first()
    File.query.filter(File.id == file.id).update({'filename': new_name})
    db.session.commit()

    return jsonify({"result": "success"})


@bp.route('/offline-download', methods=['POST'])
@login_required
def offline_download():
    params = request.json
    user_name = current_user.username
    user_id = Users.query.filter(Users.username == user_name).first().id
    path = params['path']
    url = params['url']
    time = datetime.now()
    od = OfflineDownload(path=path, url=url, completed=0, time=time, error=0, userid=user_id, done=False)
    db.session.add(od)
    db.session.commit()
    addUri.delay(od.id, [url])

    return jsonify({"result": "success", 'id': od.id})


@bp.route('/move-resource', methods=['POST'])
@login_required
def move_resource():
    params = request.json
    user_name = current_user.username
    user_id = Users.query.filter(Users.username == user_name).first().id
    file_names = params['filenames']
    path = params['path']
    new_path = params['newpath']
    directory_type_id = FileType.query.filter(FileType.filetype == 'directory').first().id
    for file_name in file_names:
        file = File.query.filter(
            File.userid == user_id, File.path == path, File.filename == file_name).first()
        if file.filetype != directory_type_id:
            file.path = new_path
        else:
            path_like = (file.path if file.path != '/' else '') + '/' + file.filename + '%'
            path_prefix = file.path  # this path is the path the need to change
            files = File.query.filter(
                File.userid == user_id,
                File.path.like(path_like)
            ).all()
            for f in files:
                print(change_path_prefix(f.path, path_prefix, new_path), f, sep=',')
                f.path = change_path_prefix(f.path, path_prefix, new_path)
            file.path = new_path
    db.session.commit()

    return jsonify({"result": "success"})


@bp.route('/search', methods=['POST'])
@login_required
def search():
    params = request.json
    path = params['path']
    query_str = params['query']
    user_name = current_user.username
    user_id = Users.query.filter(Users.username == user_name).first().id
    files = File.query.join(FileType).filter(
        File.userid == user_id, File.path.like(path + '%'), File.filename.like('%' + query_str + '%')
    ).add_columns(FileType.filetype).all()

    rv = {"result": "success", "files": []}
    for index, f in enumerate(files):
        file_item = {}
        file_item['id'] = index
        file_item['fileName'] = f.File.filename
        file_item['fileType'] = f.filetype
        file_item['fileSize'] = f.File.filesize
        file_item['modifiedTime'] = f.File.uploaddate.strftime("%Y-%m-%d %H:%M:%S")
        file_item['path'] = f.File.path
        rv['files'].append(file_item)

    return jsonify(rv)
