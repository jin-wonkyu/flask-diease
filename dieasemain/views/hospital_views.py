from flask import Blueprint, url_for, render_template

from werkzeug.utils import redirect


bp = Blueprint('hospital', __name__, url_prefix='/')


@bp.route('/hospital/')
def hospital():
    return render_template('hospital/hospital.html') # game/list/ 가져오는 것