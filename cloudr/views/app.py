from flask import Blueprint, render_template


app_bp = Blueprint('app', __name__, static_folder='../app/dist/static', template_folder='../app/dist', url_prefix='/app')


@app_bp.route('/', methods=['GET'])
def app():
    return render_template('index.html')
