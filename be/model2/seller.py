import  jwt
import time
import sqlalchemy
from be.model2.db import db
from be.model2 import error
import json

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
        book_id = self.session.execute("SELECT book_id FROM store WHERE book_id = %d;"% (int(book_id),)).fetchone()
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
            book_id=int(book_id)

            row = self.session.execute("SELECT book_id FROM book WHERE book_id = '%s';" % (book_id,)).fetchone()

            if row is None:
                book = json.loads(book_json_str)
                thelist = []  # 由于没有列表类型，故使用将列表转为text的办法
                for tag in book.get('tags'):
                    if tag.strip() != "":
                        # book.tags.append(tag)
                        thelist.append(tag)
                book['tags'] = str(thelist)  # 解析成list请使用eval(
                if book.get('picture') is not None:
                    self.session.execute(
                    "INSERT into book( book_id, title,author,publisher,original_title,translator,"
                    "pub_year,pages,original_price,currency_unit,binding,isbn,author_intro,book_intro,"
                    "content,tags,picture) VALUES ( :book_id, :title,:author,:publisher,:original_title,:translator,"
                    ":pub_year,:pages,:original_price,:currency_unit,:binding,:isbn,:author_intro,:book_intro,"
                    ":content,:tags,:picture)" , {'book_id':book['id'], 'title':book['title'],'author':book['author'],
                     'publisher':book['publisher'],'original_title':book['original_title'],'translator':book['translator'],
                    'pub_year':book['pub_year'],'pages':book['pages'],'original_price':book['price'],'currency_unit':book['currency_unit'],
                    'binding':book['binding'],'isbn':book['isbn'],'author_intro':book['author_intro'],'book_intro':book['book_intro'],
                     'content':book['content'],'tags':book['tags'],'picture':book['picture']})
                else:
                    self.session.execute(
                        "INSERT into book( book_id, title,author,publisher,original_title,translator,"
                        "pub_year,pages,original_price,currency_unit,binding,isbn,author_intro,book_intro,"
                        "content,tags) VALUES ( :book_id, :title,:author,:publisher,:original_title,:translator,"
                        ":pub_year,:pages,:original_price,:currency_unit,:binding,:isbn,:author_intro,:book_intro,"
                        ":content,:tags)",
                        {'book_id': book['id'], 'title': book['title'], 'author': book['author'],
                         'publisher': book['publisher'], 'original_title': book['original_title'],
                         'translator': book['translator'],
                         'pub_year': book['pub_year'], 'pages': book['pages'], 'original_price': book['price'],
                         'currency_unit': book['currency_unit'],
                         'binding': book['binding'], 'isbn': book['isbn'], 'author_intro': book['author_intro'],
                         'book_intro': book['book_intro'],
                         'content': book['content'], 'tags': book['tags']})


            self.session.execute("INSERT into store(store_id, book_id, stock_level,price) VALUES ('%s', %d,  %d,%d)"% (store_id, int(book_id), stock_level,price))
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_book_id(str(book_id))
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        try:
            row = self.session.execute("SELECT user_id FROM user_store WHERE store_id = '%s';" % (store_id,)).fetchone()
            if row is None:
                return error.error_non_exist_store_id(store_id)
            if row.user_id != user_id:
                return error.error_non_exist_user_id(user_id)
            if not self.check_book(book_id):
                return error.error_non_exist_book_id(book_id)
            self.session.execute("UPDATE store SET stock_level = stock_level + %d "
                                 "WHERE store_id = '%s' AND book_id = %d" % (add_stock_level, store_id, int(book_id)))
            self.session.commit()
        except ValueError:
            code, mes = error.error_non_exist_book_id(book_id)
            return code,mes
        return 200, "ok"

    def send_books(self,seller_id,order_id):
        row = self.session.execute(
            "SELECT status,store_id FROM new_order_paid  WHERE order_id = '%s'" % (order_id,)).fetchone()
        if row is None:
            return error.error_invalid_order_id(order_id)
        if row[0]!=0:
            return 521,'books has been sent to costumer'
        row = self.session.execute(
            "SELECT user_id FROM user_store WHERE store_id = '%s';" % (row[1],)).fetchone()
        if row[0]!=seller_id:
            return error.error_authorization_fail()
        self.session.execute(
            "UPDATE new_order_paid set status=1 where order_id = '%s' ;" % ( order_id))
        self.session.commit()
        return  200, "ok"


