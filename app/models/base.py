# -*- coding:utf-8 -*-
__author__ = 'neo'
__time__ = '2018/10/17 16:17'
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy,BaseQuery
from sqlalchemy import Column,Integer,SmallInteger
from contextlib import contextmanager
from datetime import datetime


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'stauts' not in kwargs.keys():
            kwargs['status']=1
        return super(Query, self).filter_by(**kwargs)



class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e



db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time',Integer)
    status = Column(SmallInteger,default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())
    def set_attrs(self,attrs_dict):
        for key,value in attrs_dict.items():
            if hasattr(self,key) and key != 'id':
                setattr(self,key,value)

    @property
    def create_datatime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def delete(self):
        self.status = 0