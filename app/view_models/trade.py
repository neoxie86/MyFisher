# -*- coding:utf-8 -*-
from .book import BookViewModel
__author__ = 'neo'
__time__ = '2018/9/14 21:26'

class TradeInfo:
    def __init__(self,goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)


    def __parse(self,goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self,single):
        if single.create_datatime:
            time = single.create_datatime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name = single.user.nickname,
            time = time,
            id = single.id
        )

# 这段是wishes和gift都要用到的，就分装到trade里面了
class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'wishes_count': count,
            'book': BookViewModel(trade.book),
            'id': trade.id
        }
        return r