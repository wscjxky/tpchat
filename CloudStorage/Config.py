#-*- coding: utf-8 -*-

HTTP_PORT = 5000
NIPServerBaseURL = 'https://nipserver-test'

DB_CONNECTOR = 'mysql+mysqlconnector'
DB_HOST = '182.92.97.97'#'182.92.97.97'
DB_PORT = '3306'
DB_USER = 'root'
DB_PASS = 'HuiTeng168'
DB_NAME = 'cloudstorage'

#心跳超时时间（超过该时间没有接收到心跳包则认为Session失效）
USER_ONLINESTATUS_UPDATE_MAX_INTERVAL = 300
#用户强制注销时间，在这段时间后没有接收到心跳包则可以在其它计算机使用该账号登陆到系统并强制将之前的登陆凭证作废
USER_LOGIN_IN_DIFF_MACHINE_MIN_INTERVAL = 80

SESSION_DIR = 'app_session'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

VISIT_FILE_FOLDER = '/fileFolders'

#存在Static文件夹下才可访问
UPLOAD_FILE_FOLDER = 'static/fileFolders/'
UPLOAD_FOLDER = 'static/image/index'
