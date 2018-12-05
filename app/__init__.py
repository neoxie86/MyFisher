# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/9 15:37'
from flask import Flask
from app.models.book import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprinter(app)

    login_manager.init_app(app)
    login_manager.login_view='web.login'
    login_manager.login_message='请先登录或注册'
    db.init_app(app)
    db.create_all(app=app)
    mail.init_app(app)
    return app

def register_blueprinter(app):
    from .web import web
    app.register_blueprint(web)