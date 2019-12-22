import  jwt
from datetime import datetime
import json
import sqlalchemy
import logging
from be.model2.db import db
from be.model2 import error
import uuid
import time
from flask import jsonify
import threading
import schedule
from datetime import timedelta
to_be_overtime={}
def overtime_append(key,value):#对to_be_overtime进行操作
    global to_be_overtime
    if key in to_be_overtime:
        to_be_overtime.append(value)
    else:
        to_be_overtime[key]=[value]

class TimerClass(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def thread(self):
        # threading.Thread(target=Buyer().auto_cancel(to_be_overtime[(datetime.utcnow() + timedelta(seconds=1)).second])).start()
        # 上面这个，有利有弊利是超过一秒也能处理 弊是每有任何一次路由访问就要延时开一次线程次数秒
        Buyer().auto_cancel(to_be_overtime[(datetime.utcnow() + timedelta(seconds=1)).second])

    def run(self):  # 每秒运行一次 将超时订单删去
        global to_be_overtime
        # schedule.every().second.do(thread)#每秒开一个线程去auto_cancel,做完的线程自动退出
        while not self.event.is_set():
            self.event.wait(1)
            if (datetime.utcnow() + timedelta(seconds=1)).second in to_be_overtime:
                self.thread()
            # schedule.run_pending()

    def cancel_timer(self):
        self.event.set()

tmr = TimerClass()
tmr.start()

def tostop():
    global tmr
    tmr.cancel_timer()


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.decode("utf-8")


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)

# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded

class Buyer():
    def __init__(self):
        db.__init__(self)

    def check_user(self, user_id):
        user = self.session.execute("SELECT user_id FROM usr WHERE user_id = '%s';" % (user_id,)).fetchone()
        if user is None:
            return False
        else:
            return True

        # 测试是否存在store

    def check_store(self, store_id):
        store = self.session.execute("SELECT store_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
        if store is None:
            return False
        else:
            return True

    def add_money(self, user_id, password, add_value):
        usr = self.session.execute("SELECT password from usr where user_id='%s'" % (user_id,)).fetchone()
        if usr is None:
            return error.error_non_exist_user_id(user_id)

        if  password != usr.password:
            return error.error_authorization_fail()
        self.session.execute(
            "UPDATE usr SET balance = balance + %d WHERE user_id = '%s'"%
            (add_value, user_id))
        self.session.commit()
        return 200, "ok"

    def order(self, user_id, store_id, id_and_count):
        try:
            order_id = ""
            if not self.check_user(user_id):
                code, mes = error.error_non_exist_user_id(user_id)
                return code, mes, order_id
            # 卖家id
            storeinfo = self.session.execute(
                "SELECT user_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
            # 存在这家店吗
            if storeinfo is None:
                code, mes = error.error_non_exist_store_id(store_id)
                return code, mes, order_id
            order_id = user_id  + str(uuid.uuid1())
            book_list = []

            for book_id, count in id_and_count:
                # 查库存
                book_id=int(book_id)
                book = self.session.execute(
                    "SELECT stock_level,price FROM store WHERE store_id = '%s' AND book_id = %d" % (
                        store_id, book_id)).fetchone()
                if book is None:
                    code, mes = error.error_non_exist_book_id(str(book_id))
                    return code, mes, " "
                if book[0] < count:
                    code, mes = error.error_stock_level_low(str(book_id))
                    return code, mes, " "
                book_list.append([book_id, count, book[1]])
            sum = 0

            for book_id, count, price in book_list:
                sum += count * price
                # 减库存，取消订单的话要加回来。
                res = self.session.execute(
                    "UPDATE store set stock_level = stock_level - %d WHERE store_id = '%s' and book_id = %d  and stock_level >=%d" % (
                        count, store_id, book_id, count))
                if res.rowcount == 0:
                    code, mes = error.error_stock_level_low(book_id)
                    return code, mes, " "
                    # 订单细节

                self.session.execute(
                    "INSERT INTO new_order_detail(order_id, book_id, count, price) VALUES('%s',%d, %d, %d);" % (
                        order_id, book_id, count, price))
            timenow = datetime.utcnow()
            # 最终下单
            self.session.execute(
                "INSERT INTO new_order_pend(order_id, buyer_id,store_id,price,pt) VALUES('%s', '%s','%s',%d,:timenow);" % (
                    order_id, user_id, store_id, sum),{'timenow':timenow})
            overtime_append(timenow.second,order_id)
            self.session.commit()
            return 200, "ok", order_id
        except ValueError:
            code, mes = error.error_non_exist_book_id(book_id)
            return code, mes, " "
        except sqlalchemy.exc.IntegrityError:
            code, mes = error.error_duplicate_bookid()
            return code, mes, " "

    def pay(self, buyer_id, password, order_id):
        # 该用户是否有这个订单代付
        row = self.session.execute(
            "SELECT buyer_id,price,store_id FROM new_order_pend WHERE order_id = '%s'" % (order_id,)).fetchone()
        if row is None:
            return error.error_invalid_order_id(order_id)
        price = row[1]
        store_id = row[2]
        if row[0] != buyer_id:
            return error.error_authorization_fail()
        # 检查密码 余额
        row = self.session.execute(
            "SELECT balance, password FROM usr WHERE user_id = '%s';" % (buyer_id)).fetchone()
        if row is None:
            return error.error_non_exist_user_id(buyer_id)
        if row[0] < price:
            error.error_not_sufficient_funds(order_id)
        if row[1] != password:
            return error.error_authorization_fail()
        # 减余额（线程安全）
        row = self.session.execute(
            "UPDATE usr set balance = balance - %d WHERE user_id = '%s' AND balance >= %d" % (
                price, buyer_id, price))
        if row.rowcount == 0:
            return error.error_not_sufficient_funds(order_id)
        # 卖家加钱
        storeinfo = self.session.execute(
            "SELECT user_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
        row = self.session.execute(
            "UPDATE usr set balance = balance + %d WHERE user_id = '%s'" % (price, storeinfo[0]))
        if row.rowcount == 0:
            return error.error_non_exist_user_id(buyer_id)
        # 删除代付订单，看是否重复付款
        row = self.session.execute("DELETE FROM new_order_pend WHERE order_id = '%s'" % (order_id,))
        if row.rowcount == 0:
            return error.error_invalid_order_id(order_id)
        # 加入已付款订单表
        timenow = datetime.utcnow()
        self.session.execute(
            "INSERT INTO new_order_paid(order_id, buyer_id,store_id,price,status,pt) VALUES('%s', '%s','%s',%d,'%s',:timenow);" % (
                order_id, buyer_id, store_id, price, 0),{'timenow':timenow})
        self.session.commit()
        return 200, "ok"

    def receive_books(self, buyer_id, order_id):
        row = self.session.execute(
            "SELECT status,buyer_id FROM new_order_paid WHERE order_id = '%s'" % (order_id,)).fetchone()
        if row is None:
            return error.error_invalid_order_id(order_id)
        if row[0] ==0:
            return 522, "book hasn't been sent to costumer"
        if row[0] ==2:
            return 523, "book has been received"
        if row[1] != buyer_id:
            return error.error_authorization_fail()
        self.session.execute(
            "UPDATE new_order_paid set status=2 where order_id = '%s' ;" % (order_id))
        self.session.commit()
        return 200, "ok"

    def search_order(self, buyer_id):
        if not self.check_user(buyer_id):
            code, mes = error.error_non_exist_user_id(buyer_id)
            return code, mes, " "
        ret=[]
        #已付款
        records=self.session.execute(
            " SELECT new_order_detail.order_id,title,new_order_detail.price,count,status,pt,new_order_paid.price "
            "FROM new_order_paid,new_order_detail,book WHERE book.book_id=new_order_detail.book_id and "
            "new_order_paid.order_id=new_order_detail.order_id and new_order_paid.buyer_id = '%s' order by new_order_detail.order_id" % (buyer_id)).fetchall()
        if len(records)!=0:
            #上一条记录的order id
            order_id_previous = records[0][0]
            statusmap = ['未发货', '已发货', '已收货']
            details=[]
            for i in range(len(records)):
                record=records[i]
                #现在的order id
                order_id_current=record[0]
                #同一个订单
                if order_id_current==order_id_previous :
                    details.append({'title':record[1],'price':record[2],'count':record[3]})
                else:
                    status=records[i-1][4]
                    ret.append({'order_id':order_id_previous,'status':statusmap[status],'time':json.dumps(records[i-1][5],cls=DateEncoder),'total_price':records[i-1][6],'detail':details})
                    details = []
                    details.append({'title': record[1], 'price': record[2], 'count': record[3]})
                order_id_previous=order_id_current
            status= records[- 1][4]
            ret.append({'order_id': order_id_previous, 'status': statusmap[status], 'time': json.dumps(records[- 1][5],cls=DateEncoder),'total_price':records[i-1][6],
                        'detail': details})
        # 未付款
        records = self.session.execute(
            "SELECT new_order_detail.order_id,title,new_order_detail.price,count,pt,new_order_pend.price "
            "FROM new_order_pend,new_order_detail,book WHERE book.book_id=new_order_detail.book_id and "
            "new_order_pend.order_id=new_order_detail.order_id and buyer_id = '%s'" % (buyer_id)).fetchall()
        if len(records)!=0:
            #上一条记录的order id
            order_id_previous = records[0][0]
            details=[]
            for i in range(len(records)):
                record=records[i]
                #现在的order id
                order_id_current=record[0]
                #同一个订单
                if order_id_current==order_id_previous :
                    details.append({'title':record[1],'price':record[2],'count':record[3]})
                else:
                    ret.append({'order_id':order_id_previous,'status':'未付款','time':json.dumps(records[i-1][4],cls=DateEncoder),'total_price':records[i-1][5],'detail':details})
                    details = []
                    details.append({'title': record[1], 'price': record[2], 'count': record[3]})
                order_id_previous=order_id_current
            ret.append({'order_id': order_id_previous, 'status':'未付款', 'time': json.dumps(records[- 1][4],cls=DateEncoder),'total_price':records[i-1][5],
                        'detail': details})
        if len(ret) != 0:
            return 200, 'ok', ret
        else:
            return 200, 'ok', " "

    def cancel(self,buyer_id, order_id):
        if not self.check_user(buyer_id):
            code, mes = error.error_non_exist_user_id(buyer_id)
            return code, mes
        #是否属于未付款订单
        store = self.session.execute("Select store_id,price FROM new_order_pend WHERE order_id = '%s' and buyer_id='%s'" % (order_id,buyer_id)).fetchone()
        if store is not None:
            store_id=store[0]
            price=store[1]
            row = self.session.execute("DELETE FROM new_order_pend WHERE order_id = '%s'" % (order_id,))
        else:
            # 是否属于已付款且未发货订单
            order_info = self.session.execute(
                "Select store_id,price FROM new_order_paid WHERE order_id = '%s' and buyer_id='%s' and status='0'" % (order_id,buyer_id)).fetchone()
            if order_info is not None:
                store_id = order_info[0]
                price = order_info[1]
                self.session.execute("DELETE FROM new_order_paid WHERE order_id = '%s' and status='0'" % (order_id,))
                # 卖家减钱
                user_id = self.session.execute(
                    "SELECT user_id FROM user_store WHERE store_id = '%s';" % (order_info[0],)).fetchone()
                self.session.execute(
                    "UPDATE usr set balance = balance - %d WHERE user_id = '%s'" % (order_info[1], user_id[0]))
                #买家加钱
                self.session.execute(
                    "UPDATE usr set balance = balance + %d WHERE user_id = '%s'" % (order_info[1], buyer_id))
            else:
                #无法取消
                return error.error_invalid_order_id(order_id)
        timenow = datetime.utcnow()
        self.session.execute(
            "INSERT INTO new_order_cancel(order_id, buyer_id,store_id,price,pt) VALUES('%s', '%s','%s',%d,:timenow);" % (
                order_id, buyer_id, store_id, price), {'timenow': timenow})
        #加库存
        self.session.execute(
                    "Update store Set stock_level = stock_level +  count from new_order_detail Where new_order_detail.book_id = store.book_id and store.store_id = '%s' and new_order_detail.order_id = '%s'" % (store_id,order_id))
        self.session.commit()
        return 200, 'ok'


    def auto_cancel(self,order_id_list):#自动取消订单
        exist_order_need_cancel=0
        #是否属于未付款订单
        for order_id in order_id_list:
            store = self.session.execute("Select buyer_id,store_id,price FROM new_order_pend WHERE order_id = '%s'" % (order_id)).fetchone()

            if store is not None:
                buyer_id=store[0]
                store_id=store[1]
                price=store[2]
                row = self.session.execute("DELETE FROM new_order_pend WHERE order_id = '%s'" % (order_id,))
                timenow = datetime.utcnow()
                self.session.execute(
                    "INSERT INTO new_order_cancel(order_id, buyer_id,store_id,price,pt) VALUES('%s', '%s','%s',%d,:timenow);" % (
                        order_id, buyer_id, store_id, price), {'timenow': timenow})
                self.session.commit()
                exist_order_need_cancel = 1
        return 'no_such_order' if exist_order_need_cancel==0 else "auto_cancel_done"