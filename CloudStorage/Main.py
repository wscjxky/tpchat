#-*- coding: utf-8 -*-
# import os

from flask import Flask, url_for, redirect, render_template


from flask.ext.restful.representations.json import settings
from flask.ext import restful
from Models import Database
from Tools import MailSender
from Tools.DataPaser import convert_to_builtin_type
from Tools.APIException import *

import sys
from Config import *

sys.path.append('/')
JSONEncoder.default = convert_to_builtin_type

app = Flask(__name__)

if sys.platform != "win32":
    app.config['SSL'] = True
    import codecs
    if sys.stdout.encoding != 'UTF-8':
        UTF8Writer = codecs.getwriter('utf8')
        sys.stdout = UTF8Writer(sys.stdout)

#app.session_interface = SqliteSessionInterface(path)

app.config['SQLALCHEMY_DATABASE_URI'] = '{0}://{1}:{2}@{3}:{4}/{5}'.format(DB_CONNECTOR, DB_USER, DB_PASS, DB_HOST,DB_PORT, DB_NAME)
app.config['SQLALCHEMY_ECHO'] = False

app.register_error_handler(Exception, all_exception_handler)
Database.db.init_app(app)
MailSender.init(app)
api = restful.Api(app)

#from Tools import ffmpegHelper
#import threading
#iconGenerator = ffmpegHelper.FFmepgThread(threading.Event())
#iconGenerator.static()

settings['ensure_ascii'] = False

import Router
Router.config(app, api)
app.add_url_rule('/<path:filename>', endpoint='/', view_func=app.send_static_file)

from Control.login import login
from Control.index import index
from Control.admin import admin
from Control.park import park

app.register_blueprint(login)         #注册蓝图
app.register_blueprint(index)
app.register_blueprint(admin)
app.register_blueprint(park)
app.secret_key = 'X0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#TODO:允许跨域调用，发布前必须注释掉，否则将有安全问题
from flask import request_started, request_finished, request


def full_dispatch_request(self):
    """Dispatches the request and on top of that performs request
    pre and postprocessing as well as HTTP exception catching and
    error handling.

    .. versionadded:: 0.7
    """
    self.try_trigger_before_first_request_functions()
    try:
        request_started.send(self)
        rv = self.preprocess_request()
        if rv is None:
            rv = self.dispatch_request()
    except Exception as e:
        rv = self.handle_user_exception(e)
    response = self.make_response(rv)
    #if request.method == 'OPTIONS':
    h = response.headers
    h['Access-Control-Allow-Origin'] = '*'
    h['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,HEAD,OPTIONS'
    #h['Access-Control-Max-Age'] = str(21600)
    #response.headers['allow'] = h['Access-Control-Allow-Methods']
    response.headers['Access-Control-Allow-Headers'] = \
        'Origin, No-Cache, X-Requested-With, If-Modified-Since, Pragma,' \
        ' Last-Modified, Cache-Control, Expires, Content-Type, X-E4M-With'
        # headers = request.headers
        # if headers is not None and not isinstance(headers, basestring):
        #     headers = ', '.join(x.upper() for x in headers)
        #     h['Access-Control-Allow-Headers'] = headers

    response = self.process_response(response)
    request_finished.send(self, response=response)
    return response


Flask.full_dispatch_request = full_dispatch_request
#TODO:允许跨域调用结束
#Tools.SessionTool.sessionApp = app

if __name__ == '__main__':
    # 调试服务才会走此流程，因为调试无法开启SSL通信所以设置为False
    app.config['SSL'] = False

    #输出当前IP，方便访问
    # import socket
    # ipList = socket.gethostbyname_ex(socket.gethostname())
    # s = "\033[1;31;0mWeb Service on http://%s:%s"
    # print s % ("127.0.0.1", HTTP_PORT)
    # for i in ipList:
    #     if isinstance(i, list):
    #         for j in i:
    #             print s % (j, HTTP_PORT)
    #     else:
    #         print s % (i, HTTP_PORT)
    #启动调试服务器

    app.run('0.0.0.0', HTTP_PORT, debug=True)
