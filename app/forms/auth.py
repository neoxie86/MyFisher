# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/17 17:31'
from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import EqualTo, Length, NumberRange, DataRequired, Email, \
    ValidationError
from app.models.user import User

class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[
        DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])

    nickname = StringField(validators=[
        DataRequired(), Length(2, 10, message='昵称至少需要两个字符，最多10个字符')])



    def validate_email(self, field):
        # db.session.
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        # db.session.
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经被使用')



class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                        Email(message='电子邮箱不符合规范')])

    password = PasswordField(validators=[
            DataRequired(message='密码不可以为空，请输入你的密码'), Length(6, 32)])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(),Length(5,64),
                                    Email(message='电子邮箱不符合规范')])



class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),
        Length(6, 32, message='密码长度至少需要在6到32个字符之间'),
        EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[
        DataRequired(), Length(6, 32)])