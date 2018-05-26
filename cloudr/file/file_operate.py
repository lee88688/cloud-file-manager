import os
from datetime import datetime
from werkzeug.utils import secure_filename 
from flask import send_from_directory, current_app, request, jsonify, session
from cloudr import model, db
from . import bp


@bp.route("/downloads/<filemd5>", methods=["POST", "GET"])
def file_download(filemd5):
    return send_from_directory(current_app.config['FILE_PATH'], filemd5)


@bp.route("/uploads", methods=["POST"])
def file_upload():
    # user_id = session['userid']
    user_id = int(request.form['userid'])
    filetype = 1
    file = request.files['file']
    size = int(request.form['filesize'])
    path = request.form['path']
    md5 = request.form['md5']
    upload_date = datetime.now()
    file_name = secure_filename(file.filename)

    file_item = model.File(userid=user_id, filetype=filetype, filename=file_name, filesize=size, uploaddate=upload_date, path=path, md5=md5)
    try:
        db.session.add(file_item)
        db.session.commit()
        file.save(os.path.join(current_app.config['FILE_PATH'], md5))
    except Exception:
        return jsonify({"result": "upload fail."})
    return jsonify({"result": "upload sucessful."})