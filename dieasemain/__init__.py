from flask import Flask
from flask_migrate import Migrate #db작업
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

# 이주를 준비함

def create_app():
    app = Flask(__name__)
    app.config.from_envvar('APP_CONFIG_FILE')
    # ORM db와 마이그레이트를 초기화함
    db.init_app(app) #초기화 하는 부분
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)
    # 블루프린트 만들기

    from dieasemain.views import auth_views
    from dieasemain.views import main_views
    from dieasemain.views import question_views
    from dieasemain.views import answer_views
    from dieasemain.views import game_views
    from dieasemain.views import com_views
    from dieasemain.views import timer_views
    from dieasemain.views import health_views
    from dieasemain.views import hospital_views
    from dieasemain.views import yak_views
    from dieasemain.views import predict_views
    from dieasemain.actions import predict_action


    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(game_views.bp)
    app.register_blueprint(com_views.bp)
    app.register_blueprint(timer_views.bp)
    app.register_blueprint(health_views.bp)
    app.register_blueprint(hospital_views.bp)
    app.register_blueprint(yak_views.bp)
    app.register_blueprint(predict_views.bp)
    app.register_blueprint(predict_action.bp)

    # 필터
    from dieasemain.filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
