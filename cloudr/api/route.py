from flask import jsonify, request
from cloudr import db
from . import bp


@bp.route("/hello", methods=["GET", "POST"])
def hello():
    return jsonify(greet="hello")