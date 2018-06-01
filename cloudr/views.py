from flask import url_for, current_app, Blueprint, render_template


bp = Blueprint("views", __name__)

@bp.route("/login")
def login():
    return render_template('login.html')