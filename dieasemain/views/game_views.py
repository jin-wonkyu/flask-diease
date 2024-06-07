from flask import Blueprint, url_for, render_template

from werkzeug.utils import redirect


bp = Blueprint('game', __name__, url_prefix='/')


@bp.route('/game/')
def list():
    return render_template('game/list.html') # game/list/ 가져오는 것