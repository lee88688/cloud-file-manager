from flask import Blueprint, render_template, request, redirect, jsonify
from cloudr.model import Users
from flask_login import login_user


view_bp = Blueprint("views", __name__)


@view_bp.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']
        user = Users.query.filter(Users.username == user_name).first()
        if user and user.password == password:
            login_user(user)
            return redirect('/app')
        else:
            return jsonify({"result": "invalid name or password."})

    return render_template('login.html')

# debug with webpack dev server $.post('/login', 'username=lee&password=1234')


@view_bp.route('/video')
def video():
    return render_template('video.html')
