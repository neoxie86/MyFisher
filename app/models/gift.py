# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/17 15:51'

from sqlalchemy import Column,Integer,String,ForeignKey,Boolean,desc,func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from app.models.base import Base
from flask import current_app
from app.spider.yushu_book import YuShuBook
from app.models.base import db
from app.models.wish import Wish


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('user.id'))
    launched = Column(Boolean, default=False)

    def is_yourself_gift(self,uid):
        return True if self.uid == uid else False

    @classmethod
    def recent(cls):
        recent_gift = Gift.query.filter_by(launched=False).group_by(Gift.isbn).order_by(
            desc(Gift.create_time)).limit(current_app.config['REENET_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False, Wish.isbn.in_(
            isbn_list), Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list