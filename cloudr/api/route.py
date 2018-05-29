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
    user_name = 'lee'
    path = request.form['path']
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
        file_item['modifiedTime'] = f.File.uploaddate
        rv['files'].append(file_item)
    
    return jsonify(rv)


@bp.route("delete-resource", methods=["POST"])
def delete_resource():
    dir_file_type = FileType.query.filter(FileType.filetype == 'directory').first().id
    user_name = request.form['userName']
    path = request.form['path']  # todo: path check
    file_name = request.form['filName']
    file = File.query.join(Users).join(FileType).\
                      filter(Users.username == user_name).\
                      filter(File.path == path).\
                      filter(File.filename == file_name).first()
    if file:
        if file.filetype != dir_file_type:
            File.query.filter(File.id == file.id).delete()
        else:
            # todo: delete the whole directory
            pass
    else:
        pass


@bp.route("new-directory", methods=["POST"])
def new_directory():
    user_name = request.form['userName']
    size = 0
    path = request.form['path']  # todo: path check
    md5 = request.form['md5']
    upload_date = datetime.now()
    file_name = secure_filename(request.files['dirName'])
    file_type = FileType.query.filter(FileType.filetype == 'directory').first().id
    user_id = Users.query.filter(Users.username == user_name).first().id  # todo: catch user_name is not found

    file = File(userid=user_id, filetype=file_type, filename=file_name, filesize=size, uploaddate=upload_date, path=path, md5=md5)
    db.session.add(file)
    db.session.commit()

    return jsonify({"result": "success"})


@bp.route("rename-resource", methods=["POST"])
def rename_resource():
    new_name = secure_filename(request.form['new-name'])
    old_name = request.form['old-name']
    path = request.form['path']
    user_name = request.form['uname']

    File.query.join(Users).filter(Users.username == user_name, 
                                  File.path == path, 
                                  File.filename == old_name).update({'filename': new_name})