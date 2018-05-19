import os
from werkzeug.utils import secure_filename 
from flask import send_from_directory, current_app, request, jsonify
from . import bp


@bp.route("/downloads/<filename>", methods=["POST", "GET"])
def file_download(filename):
    return send_from_directory(current_app.config['FILE_PATH'], filename)


@bp.route("/uploads", methods=["POST"])
def file_upload():
    file = request.files['file']
    file_name = secure_filename(file.filename)
    file.save(os.path.join(current_app.config['FILE_PATH'], file_name))
    return jsonify({"result": "upload sucessful."})