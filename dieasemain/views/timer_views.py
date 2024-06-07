from flask import Blueprint, url_for, render_template

from werkzeug.utils import redirect


bp = Blueprint('time', __name__, url_prefix='/')


@bp.route('/time/')
def timer():
    return render_template('time/timer.html') # game/list/ 가져오는 것