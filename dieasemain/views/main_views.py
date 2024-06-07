from flask import Blueprint, render_template, url_for
from dieasemain.models import Question
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/') #프리픽스는 접두사같은 개념이다.


@bp.route('/') # 얘네들이 컨트롤러 개념임
def index():
    return render_template('index.html') # html로 보내고
#
# @bp.route('/')
# def index():
#     return redirect(url_for('question._list'))
#     # question/list/ 가져오는 것
