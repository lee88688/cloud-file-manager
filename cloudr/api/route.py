import hashlib
from datetime import datetime
from flask import jsonify, request
from werkzeug.utils import secure_filename 
from cloudr import db
from cloudr.model import File, Users, FileType
from . import bp


@bp.route("/hello", methods=["GET", "POST"])
def hello():
    return jsonify(greet="hello")


@bp.route("/get-path-content", methods=["POST"])
def get_path_content():
    # user_name = request.form['uname']
    user_name = 'lee'  # todo: user name
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
        rv['files'].append(file_item)
    
    return jsonify(rv)


@bp.route("/delete-resource", methods=["POST"])
def delete_resource():
    dir_file_type = FileType.query.filter(FileType.filetype == 'directory').first().id
    user_name = "lee"  # todo: get user name
    path = request.json['path']  # todo: path check
    file_list = request.json["fileList"]
    for file_name in file_list:
        file = File.query.join(Users).join(FileType).\
                        filter(Users.username == user_name).\
                        filter(File.path == path).\
                        filter(File.filename == file_name).first()
        if file:
            if file.filetype != dir_file_type:
                File.query.filter(File.id == file.id).delete()
                # todo: need to remove real file.
            else:
                # todo: delete the whole directory
                pass
        else:
            pass
    db.session.commit()
    return jsonify({"result": "success"})


@bp.route("/new-directory", methods=["POST"])
def new_directory():
    user_name = "lee"  # todo: get current user name.
    size = 0
    path = request.json['path']  # todo: path check
    md5 = "-"
    upload_date = datetime.now()
    file_name = secure_filename(request.json['dirName'])
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
def rename_resource():
    new_name = secure_filename(request.json['newname'])
    old_name = request.json['oldname']
    path = request.json['path']
    user_name = "lee"  # todo: get current user name.

    file = File.query.join(Users).filter(Users.username == user_name, 
                                       File.path == path, 
                                       File.filename == old_name).first()
    File.query.filter(File.id == file.id).update({'filename': new_name})
    db.session.commit()

    return jsonify({"result": "success"})