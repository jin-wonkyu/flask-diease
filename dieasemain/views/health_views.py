from flask import Blueprint, url_for, render_template

from werkzeug.utils import redirect


bp = Blueprint('health', __name__, url_prefix='/')


@bp.route('/health/')
def list():
    return render_template('health/health.html') # com/list/ 가져오는 것

