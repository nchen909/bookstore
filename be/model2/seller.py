import  jwt
import time
import sqlalchemy
from be.model2.db import db
from be.model2 import error

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

class Seller():
    def __init__(self):
        db.__init__(self)
    #测试是否存在usr
    def check_user(self, user_id):
        user = self.session.execute("SELECT user_id FROM usr WHERE user_id = '%s';"% (user_id,)).fetchone()
        if user is None:
            return False
        else:
            return True

    # 测试是否存在store
    def check_store(self,store_id):
        store = self.session.execute("SELECT store_id FROM user_store WHERE store_id = '%s';"% (store_id,)).fetchone()
        if store is None:
            return False
        else:
            return True

    # 测试是否存在book
    def check_book(self,book_id):
        book_id = self.session.execute("SELECT book_id FROM user_store WHERE book_id = '%s';"% (book_id,)).fetchone()
        if book_id is None:
            return False
        else:
            return True

    def create_store(self, user_id: str, store_id: str):
        try:
            if not self.check_user(user_id) :
                return error.error_non_exist_user_id(user_id)
            self.session.execute("INSERT into user_store(store_id, user_id) VALUES ('%s', '%s')"%(store_id, user_id))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_store_id(store_id)
        return 200, "ok"

    def add_book(self, user_id: str, store_id: str, book_id: str, price:int,book_json_str: str, stock_level: int):
        try:
            if not self.check_user(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.check_store(store_id):
                 return error.error_non_exist_store_id(store_id)
            self.session.execute("INSERT into store(store_id, book_id, book_info, stock_level,price) VALUES ('%s', '%s', '%s', %d,%d)"% (store_id, book_id, book_json_str, stock_level,price))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_book_id(book_id)
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        row = self.session.execute("SELECT user_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
        if row is None:
            return error.error_non_exist_store_id(store_id)
        if row.user_id!=user_id:
            return error.error_non_exist_user_id(user_id)
        if not self.check_book(book_id):
            return error.error_non_exist_book_id(book_id)
        self.session.execute("UPDATE store SET stock_level = stock_level + %d "
                          "WHERE store_id = '%s' AND book_id = '%s'", (add_stock_level, store_id, book_id))
        self.session.commit()