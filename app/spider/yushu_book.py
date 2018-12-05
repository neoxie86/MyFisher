# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/9 14:38'

from flask import current_app

from app.libs.httper import HTTP


class YuShuBook(object):
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.total = 0
        self.books = []

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        if data:
            self.total = data['total']
            self.books = data['books']


    def search_by_isbn(self,isbn):
        result = HTTP.get(self.isbn_url.format(isbn))
        self.__fill_single(result)



    def search_by_keyword(self,keyword,page=1):
        result = HTTP.get(self.keyword_url.format(keyword,current_app.config['PER_PAGE']
                                                 ,self.calculate_start(page)))
        self.__fill_collection(result)

    @staticmethod
    def calculate_start(page):
        return (page - 1) * current_app.config['PER_PAGE']

    @property
    def first(self):
        return self.books[0] if self.total >=1 else None