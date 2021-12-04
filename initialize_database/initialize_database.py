from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint, Text, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker

import psycopg2
from datetime import datetime,time
import sys
sys.path.append('..')
from bookstore.config import Conf
# 连接数据库legend 记得修改这个！！！
#engine = create_engine(Conf.get_sql_conf('local_w'))
engine = create_engine(Conf.get_sql_conf('local_y'))
#engine = create_engine(Conf.get_sql_conf('local'))

Base = declarative_base()


# String长度可能需要做修改
# 用户表
class User(Base):
    __tablename__ = 'usr'
    user_id = Column(String(128), primary_key=True)
    password = Column(String(128), nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(String(400), nullable=False)
    terminal = Column(String(256), nullable=False)


# 商店表（含书本信息）
class Store(Base):
    __tablename__ = 'store'
    store_id = Column(String(128), ForeignKey('user_store.store_id'), nullable=False, index = True)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, index = True)
    stock_level = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)  # 售价
    __table_args__ = (
        PrimaryKeyConstraint('store_id', 'book_id'),
        {},
    )


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    original_price = Column(Integer)  # 原价
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    picture = Column(LargeBinary)

# 用户商店关系表
class User_store(Base):
    __tablename__ = 'user_store'
    user_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False, index = True)
    store_id = Column(String(128), nullable=False, unique=True, index = True) # 这里的store不可能重复
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'store_id'),
        {},
    )


# 未付款订单
class New_order_pend(Base):
    __tablename__ = 'new_order_pend'
    order_id = Column(String(128), primary_key=True)
    buyer_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    store_id = Column(String(128), ForeignKey('user_store.store_id'), nullable=False)
    price = Column(Integer, nullable=False)
    pt = Column(DateTime, nullable=False)


# 已取消订单
class New_order_cancel(Base):
    __tablename__ = 'new_order_cancel'
    order_id = Column(String(128), primary_key=True)
    buyer_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    store_id = Column(String(128), ForeignKey('user_store.store_id'), nullable=False)
    price = Column(Integer, nullable=False)
    pt = Column(DateTime, nullable=False)


# 已付款订单
class New_order_paid(Base):
    __tablename__ = 'new_order_paid'
    order_id = Column(String(128), primary_key=True)
    buyer_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    store_id = Column(String(128), ForeignKey('user_store.store_id'), nullable=False)
    price = Column(Integer, nullable=False)
    pt = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)  # 0为待发货，1为已发货，2为已收货


# 订单中的书本信息
class New_order_detail(Base):
    __tablename__ = 'new_order_detail'
    order_id = Column(String(128), nullable=False)
    book_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('order_id', 'book_id'),
        {},
    )


def init():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    # 提交即保存到数据库
    session.commit()
    # 关闭session
    session.close()


def add_info():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # 提交即保存到数据库A
    A = User(user_id = '王掌柜',
            password = '123456',
            balance = 100,
            token = '***',
            terminal = 'Edge')
    B = User(user_id = '小明',
            password = '123456',
            balance = 500,
            token = '***',
            terminal='Chrome')
    session.add_all([A, B])
    session.commit()

    A_Store1 = User_store(user_id = '王掌柜',
                        store_id = '王掌柜的书店')
    A_Store2 = User_store(user_id = '王掌柜',
                        store_id = '王掌柜的进口书店')
    # Book1 = Book(book_id = 0,
    #             title='数据结构')
    # Book2 = Book(book_id=1,
    #             title='PRML')
    # session.add_all([A_Store1, A_Store2, Book1, Book2])
    session.add_all([A_Store1, A_Store2])
    session.commit()

    StoreA = Store(store_id = '王掌柜的书店',
                    book_id = 1,
                    stock_level=10,
                    price=1000) # 价格单位是分
    StoreB = Store(store_id = '王掌柜的进口书店',
                    book_id = 2,
                    stock_level=10,
                    price=10000)
    session.add_all([StoreA, StoreB])
    session.commit()
    
    OrderA = New_order_paid(order_id = 'order1',
                            buyer_id = '小明',
                            store_id = '王掌柜的书店',
                            price=2000,
                            pt = datetime.now(),
                            status = 0)  # 0为已付款，1为已发货，2为已收货
    Order_detailA = New_order_detail(order_id = 'order1',
                                    book_id = 1,
                                    count = 2,
                                    price = 2000)
    OrderB = New_order_pend(order_id = 'order2',
                            buyer_id = '小明',
                            store_id = '王掌柜的进口书店',
                            price = 10000,
                            pt = datetime.now())
    Order_detailB = New_order_detail(order_id = 'order2',
                                    book_id = 2,
                                    count = 1,
                                    price = 10000)
    session.add_all([OrderA, Order_detailA, OrderB, Order_detailB])
    session.commit()
    # 关闭session
    session.close()


if __name__ == "__main__":
    # 创建数据库
    init()
    # 加入信息
    add_info()

