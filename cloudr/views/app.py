from flask import Blueprint, render_template
from flask_login import login_required


app_bp = Blueprint('app', __name__, static_folder='../app/dist/static', template_folder='../app/dist', url_prefix='/app')


@app_bp.route('/', methods=['GET'])
@login_required
def app():
    return render_template('index.html')
