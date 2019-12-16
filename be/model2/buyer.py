import  jwt
from datetime import datetime

import sqlalchemy
import logging
from be.model2.db import db
from be.model2 import error
import uuid
def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.decode("utf-8")

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
                "INSERT INTO new_order_pend(order_id, buyer_id,seller_id,price,pt) VALUES('%s', '%s','%s',%d,:timenow);" % (
                    order_id, user_id, storeinfo[0], sum),{'timenow':timenow})
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
            "SELECT buyer_id,price,seller_id FROM new_order_pend WHERE order_id = '%s'" % (order_id,)).fetchone()
        if row is None:
            return error.error_invalid_order_id(order_id)
        price = row[1]
        seller_id = row[2]
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
        row = self.session.execute(
            "UPDATE usr set balance = balance + %d WHERE user_id = '%s'" % (price, seller_id))
        if row.rowcount == 0:
            return error.error_non_exist_user_id(buyer_id)
        # 删除代付订单，看是否重复付款
        row = self.session.execute("DELETE FROM new_order_pend WHERE order_id = '%s'" % (order_id,))
        if row.rowcount == 0:
            return error.error_invalid_order_id(order_id)
        # 加入已付款订单表
        timenow = datetime.utcnow()
        self.session.execute(
            "INSERT INTO new_order_paid(order_id, buyer_id,seller_id,price,status,pt) VALUES('%s', '%s','%s',%d,'%s',:timenow);" % (
                order_id, buyer_id, seller_id, price, 0),{'timenow':timenow})
        self.session.commit()

        return 200, "ok"

    def receive_books(self, buyer_id, order_id):
        row = self.session.execute(
            "SELECT status,buyer_id FROM new_order_paid WHERE order_id = '%s'" % (order_id,)).fetchone()
        if row is None:
            return error.error_invalid_order_id(order_id)
        if row[0] != 1:
            return 522, "book hasn't been sent to costumer"
        if row[1] != buyer_id:
            return error.error_authorization_fail()
        self.session.execute(
            "UPDATE new_order_paid set status=2 where order_id = '%s' ;" % (order_id))
        self.session.commit()
        return 200, "ok"