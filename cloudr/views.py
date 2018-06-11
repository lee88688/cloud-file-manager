from flask import url_for, current_app, Blueprint, render_template, request, redirect, jsonify
from .model import Users


bp = Blueprint("views", __name__)

@bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        user = Users.query.filter(Users.username == user_name).first()
        if user and user.password == password:
            redirect('/index')
        else:
            return jsonify({"result": "invalid name or password."})

    return render_template('login.html')