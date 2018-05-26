from flask import jsonify, request
from cloudr import db
from cloudr.model import File, Users, FileType
from . import bp


@bp.route("/hello", methods=["GET", "POST"])
def hello():
    return jsonify(greet="hello")


@bp.route("/get-path-content", methods=["POST"])
def get_path_content():
    user_name = request.form['uname']
    path = request.form['path']
    File.query.join(Users).join(FileType).filter(Users.username == user_name, File.path == path).add_column(FileType.filetype)


@bp.route("delete-resource", methods=["POST"])
def delete_resource():
    pass


@bp.route("new-directory", methods=["POST"])
def new_directory():
    pass


@bp.route("rename-resource", methods=["POST"])
def rename_resource():
    new_name = request.form['new-name']
    old_name = request.form['old-name']
    path = request.form['path']
    user_name = request.form['uname']

    File.query.join(Users).filter(Users.username == user_name, 
                                    File.path == path, 
                                    File.filename == old_name).update({'filename': new_name})