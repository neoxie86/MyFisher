# -*- coding:utf-8 -*-
from app import mail
from flask_mail import Message
from flask import current_app,render_template
from threading import Thread

__author__ = 'neo'
__time__ = '2018/9/19 14:51'


def send_async_email(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)

def send_mail(to,subject,template,**kwargs):
    # msg = Message('test',sender='xiebin_neo@163.com',body='test',recipients=['254903295@qq.com'])
    msg = Message('test'+''+subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template,**kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    # mail.send(msg)
