import os
# os는 시스템 모듈, 기능이 많음

BASE_DIR = os.path.dirname(__file__)
#URI는 데이터베이스 접속 주소.
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'board.db')) # board.db는 db명임, 디비명을 설정한것
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"