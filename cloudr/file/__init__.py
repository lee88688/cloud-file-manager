from flask import Blueprint


bp = Blueprint("file", __name__, url_prefix="/file")

from . import file_operate