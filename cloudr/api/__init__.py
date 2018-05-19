from flask import Blueprint


bp = Blueprint("api", __name__, url_prefix="/api")

from . import route
from . import file_operate