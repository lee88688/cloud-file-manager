import os
import math
from datetime import datetime
from werkzeug.utils import secure_filename 
from flask import send_from_directory, current_app, request, jsonify, session, abort
from flask_login import current_user
from cloudr import model
from cloudr.model import db, File, Users, UploadCache
from cloudr.utils.filetype import check_file_type
from cloudr.utils import api_result, SUCCESS_RESULT, FAILURE_RESULT
from cloudr.config import SPLIT_SIZE
from . import bp


# @bp.route("/downloads/<filemd5>", methods=["POST", "GET"])
# def file_download(filemd5):
#     return send_from_directory(current_app.config['FILE_PATH'], filemd5)


@bp.route("/download", methods=["GET"])
def file_download():
    user_name = 'lee'
    path = request.args.get('path')
    filename = request.args.get('filename')
    file = File.query.join(Users).filter(
        Users.username == user_name,
        File.filename == filename,
        File.path == path
    ).first()
    if not file:
        abort(404)
    return send_from_directory(current_app.config['FILE_PATH'], file.md5, as_attachment=True, attachment_filename=filename, conditional=True)


@bp.route("/uploads", methods=["POST"])
def file_upload():
    blob = request.files['blob']
    try:
        uc = UploadCache.load(request.form['task_id'])
    except Exception:
        return jsonify(api_result(FAILURE_RESULT, 'upload task may be expired. restart a new upload later.'))

    uc.cache.append(blob)
    if not uc.saving_task_start:
        # todo: start saving task
        pass
    return jsonify(api_result(SUCCESS_RESULT))


@bp.route('/upload-request', methods=["POST"])
def upload_request():
    try:
        user_id = current_user.id
    except AttributeError:
        abort(404)
    file = request.files['file']
    size = int(request.form['filesize'])
    path = request.form['path']
    md5 = request.form['md5']
    upload_date = datetime.now()
    file_name = file.filename
    file_type_name = check_file_type(file_name)
    filetype = model.FileType.query.filter(model.FileType.filetype == file_type_name).first()
    if not filetype:
        return jsonify(api_result("failure", "can't identify the file type."))
    filetype = filetype.id

    max_sequence_number = math.ceil(size / SPLIT_SIZE)
    uc = UploadCache.create(
        id=UploadCache.generate_id(),
        max_sequence_number=max_sequence_number,
        size=size,
        path=path,
        md5=md5,
        upload_date=upload_date,
        file_name=file_name,
        filetype=filetype,
        user_id=user_id
    )

    return jsonify(api_result(SUCCESS_RESULT, task_id=uc.id, split_size=SPLIT_SIZE))
