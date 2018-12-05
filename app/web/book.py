# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/9 15:37'
from flask import  jsonify,request,flash

from app.forms.book import SearchForm
from app.libs.helper import is_isbn_key
from app.spider.yushu_book import YuShuBook
from . import web
from app.view_models.book import BookViewModel,BookCollection
import json
from flask import render_template
from flask_login import current_user
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo


@web.route('/book/search')
def search():
    form = SearchForm(request.args)
    books = BookCollection()
    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_key(q)
        yushubook = YuShuBook()
        if isbn_or_key == 'isbn':
            yushubook.search_by_isbn(q)
        else:
            yushubook.search_by_keyword(q,page)
        books.fill(yushubook,q)
        # return json.dumps(books,default=lambda o:o.__dict__)
        # return jsonify(books)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html',books=books,form=form)



@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html',
                           book=book, wishes=trade_wishes_model,
                           gifts=trade_gifts_model, has_in_wishes=has_in_wishes,
                           has_in_gifts=has_in_gifts)


@web.route('/test/')
def test():
    r = {
        'name':'neo',
        'age':18
    }
    flash('ok')
    return render_template('test.html',data=r)