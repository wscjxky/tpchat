#-*- coding: utf-8 -*-
import threading

from flask_mail import Mail, Message

mail = Mail()

def init(app):
    app.config['MAIL_SERVER'] = 'smtp.163.com'
    app.config['MAIL_USERNAME'] = 'HT_Multimedia'
    app.config['MAIL_PASSWORD'] = 'ht123456'
    app.config['MAIL_DEFAULT_SENDER'] = 'HT_Multimedia@163.com'
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_DEBUG'] = True
    app.config['MAIL_PORT'] = 25 #发送为110，接收为25
    mail.init_app(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_mail(app, body='', html='', recipients=[], subject=''):
    msg = Message(body=body, html=html, recipients=recipients, subject=subject)
    mail.send(msg)
    return "ok"

# def send_mail(app, body='', html='', recipients=[], subject=''):
#     thr = threading.Thread(target=send_async_email, args=[app, Message(body=body, html=html,
#                                                                   recipients=recipients, subject=subject)])
#     thr.start()