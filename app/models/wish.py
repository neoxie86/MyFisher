# -*- coding:utf-8 -*-
from sqlalchemy import Column,Integer,Boolean,String,ForeignKey,desc,func
from sqlalchemy.orm import relationship
from app.models.base import Base,db

from app.spider.yushu_book import YuShuBook

__author__ = 'neo'
__time__ = '2018/9/12 11:00'

class Wish(Base):
    id = Column(Integer,primary_key=True)
    user = relationship('User')
    uid = Column(Integer,ForeignKey('user.id'))
    #数据库中并没有book，直接用接口返回的数据
    # book = relationship('Book')
    # bid = Column(Integer,ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean,default=False)


    @classmethod
    def get_user_wishes(cls,uid):
        wishes = Wish.query.filter_by(uid=uid,launched=False).order_by(
            desc(Wish.create_time)).all()
        return wishes

    @classmethod
    def get_gift_counts(cls,isbn_list):
        from app.models.gift import Gift
        count_list = db.session.query(func.count(Gift.id),Gift.isbn).filter(Gift.launched == False,Gift.isbn.in_(
            isbn_list),Gift.status==1).group_by(Gift.isbn).all()
        count_list = [{'count':w[0],'isbn':w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first


    # @classmethod
    # def recent(cls):
    #     recent_gift = Gift.query.filter_by(launched = False).group_by(Gift.isbn).order_by(
    #         desc(Gift.create_time)).limit(current_app.config['REENET_BOOK_COUNT']).distinct().all()
    #     return recent_gift