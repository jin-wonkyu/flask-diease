from flask import Blueprint, url_for, render_template

from werkzeug.utils import redirect


bp = Blueprint('com', __name__, url_prefix='/')


@bp.route('/com/')
def list():
    return render_template('com/list.html') # com/list/ 가져오는 것

