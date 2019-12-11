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
        order_id = ""
        if not self.check_user(user_id):
            code, mes = error.error_non_exist_user_id(user_id)
            return code, mes, order_id
        storeinfo = self.session.execute(
            "SELECT user_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
        if storeinfo is None:
            code, mes = error.error_non_exist_store_id(store_id)
            return code, mes, order_id
        order_id = user_id + str(uuid.uuid1())
        book_list = []
        
        for book_id, count in id_and_count:
            book = self.session.execute(
                "SELECT stock_level,price FROM store WHERE store_id = '%s' AND book_id = '%s';" % (
                    store_id, book_id)).fetchone()
            if book is None:
                code, mes = error.error_non_exist_book_id(book_id)
                return code, mes, ""
            if book[0] < count:
                code, mes = error.error_stock_level_low(book_id)
                return code, mes, ""
            book_list.append([book_id, count, book[1]])
        sum = 0
        for book_id, count, price in book_list:
            sum += count * price
            self.session.execute(
                "UPDATE store set stock_level = stock_level - %d WHERE store_id = '%s' and book_id = '%s' " % (
                    count, store_id, book_id))
            self.session.execute(
                "INSERT INTO new_order_detail(order_id, book_id, count, price) VALUES('%s', '%s', %d, %d);" % (
                    order_id, book_id, count, price))
        timenow =  datetime.utcnow()
        self.session.execute(
            "INSERT INTO new_order_pend(order_id, buyer_id,seller_id,price,pt) VALUES('%s', '%s','%s',%d,'%s');" % (
                order_id, user_id, storeinfo[0], sum, timenow))
        self.session.commit()
        return 200, "ok",order_id