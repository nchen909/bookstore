from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint,Text,TIMESTAMP
from sqlalchemy.orm import sessionmaker
import psycopg2
# 连接数据库legend 记得修改这个！！！
# engine = create_engine('postgresql://postgres:amyamy@localhost:5433/bookstore')
engine = create_engine('postgresql://postgres:990814@[2001:da8:8005:4056:81e9:7f6c:6d05:fe47]:5432/bookstore')
Base = declarative_base()
# String长度可能需要做修改
# 用户表
class User(Base):
    __tablename__ = 'usr'
    user_id = Column(String(128), primary_key=True)
    password = Column(String(128), nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(String(400))
    terminal = Column(String(64))

# 商店表（含书本信息）
class Store(Base):
    __tablename__ = 'store'
    store_id = Column(String(128), nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)
    stock_level = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('store_id', 'book_id'),
        {},
    )

# 用户商店关系表
class User_store(Base):
    __tablename__ = 'user_store'
    user_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    store_id = Column(String(128), nullable=False)
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'store_id'),
        {},
    )

# 未付款订单
class New_order_pend(Base):
    __tablename__ = 'new_order_pend'
    order_id = Column(String(128), primary_key=True)
    buyer_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    seller_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    price = Column(Integer, nullable=False)
    pt=Column(TIMESTAMP, nullable=False)

# 已取消订单
class New_order_cancel(Base):
    __tablename__ = 'new_order_cancel'
    order_id = Column(String(128), primary_key=True)
    buyer_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    seller_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    price = Column(Integer, nullable=False)

# 已付款订单
class New_order_paid(Base):
    __tablename__ = 'new_order_paid'
    order_id = Column(String(128), primary_key=True)
    buyer_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    seller_id = Column(String(128), ForeignKey('usr.user_id'), nullable=False)
    price = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

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
    A = User(user_id = 'A',
            password = '123456',
            balance = 100,
            token = 'AAA',
            terminal = 'AAA')
    B = User(user_id = 'B',
            password = '123456',
            balance = 500,
            token = 'BBB',
            terminal='BBB')
    StoreA = Store(store_id = 'StoreA',
                    book_id = 'BookA',
                    book_info='A nice book.',
                    stock_level=10,
                    price=10)
    StoreB = Store(store_id = 'StoreB',
                    book_id = 'BookA',
                    book_info='A nice book.',
                    stock_level=10,
                    price=10)
    session.add_all([A, B ,StoreA])
    session.commit()
    A_Store1 = User_store(user_id = 'A',
                        store_id = 'StoreA')
    A_Store2 = User_store(user_id = 'A',
                        store_id = 'StoreB')
    OrderA = New_order_paid(order_id = 'order1',
                            buyer_id = 'B',
                            seller_id = 'A',
                            price = 20,
                            status = 'Already evaluated')  # 或者Send goods 或者Received goods
    Order_detailA = New_order_detail(order_id = 'order1',
                                    book_id = 'BookA',
                                    count = 2,
                                    price = 20)
    session.add_all([
        A_Store1, A_Store2, OrderA, Order_detailA
    ])
    session.commit()
    # 关闭session
    session.close()

if __name__ == "__main__":
    # 创建数据库
    init()
    # 加入信息
    #add_info()