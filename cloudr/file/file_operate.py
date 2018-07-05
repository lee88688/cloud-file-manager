import os
from datetime import datetime
from werkzeug.utils import secure_filename 
from flask import send_from_directory, current_app, request, jsonify, session
from cloudr import model
from cloudr.model import db, File, Users
from cloudr.utils.filetype import check_file_type
from cloudr.utils import api_result
from . import bp


# @bp.route("/downloads/<filemd5>", methods=["POST", "GET"])
# def file_download(filemd5):
#     return send_from_directory(current_app.config['FILE_PATH'], filemd5)


@bp.route("/downloads", methods=["GET"])
def file_download():
    user_name = 'lee'
    path = request.args.get('path')
    filename = request.args.get('filename')
    file = File.query.join(Users).filter(
        Users.username == user_name,
        File.filename == filename,
        File.path == path
    ).first()
    return send_from_directory(current_app.config['FILE_PATH'], file.md5, as_attachment=True, attachment_filename=filename)


@bp.route("/uploads", methods=["POST"])
def file_upload():
    # user_id = int(request.form['userid'])
    user_id = 1  # get current user
    file = request.files['file']
    size = int(request.form['filesize'])
    path = request.form['path']
    md5 = request.form['md5']
    upload_date = datetime.now()
    # file_name = secure_filename(file.filename)
    file_name = file.filename
    file_type_name = check_file_type(file_name)
    filetype = model.FileType.query.filter(model.FileType.filetype == file_type_name).first()
    if not filetype:
        return jsonify(api_result("failure", "can't identify the file type."))
    filetype = filetype.id

    file_item = model.File(userid=user_id, filetype=filetype, filename=file_name, filesize=size, uploaddate=upload_date, path=path, md5=md5)
    try:
        db.session.add(file_item)
        db.session.commit()
        file.save(os.path.join(current_app.config['FILE_PATH'], md5))
    except Exception:
        return jsonify(api_result("failure", "upload fail."))
    return jsonify(api_result("success"))
