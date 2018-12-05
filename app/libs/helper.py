# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/9 10:36'

def is_isbn_key(word):
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-','')
    if '-' in word and len(short_word)==10 and short_word.isdigit():
        isbn_or_key = 'isbn'
    return isbn_or_key