from flask import jsonify
from cloudr import db
from . import bp


@bp.route("/hello", methods=["GET"])
def hello():
    return jsonify(greet="hello")