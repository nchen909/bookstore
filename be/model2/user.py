import base64

import  jwt
import time
import sqlalchemy
from be.model2.db import db
from be.model2 import error
# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


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


class User():
    def __init__(self):
        db.__init__(self)



    def register(self, user_id: str, password: str):
        terminal = "terminal_{}".format(str(time.time()))
        try:
            token=""
            self.session.execute(  "INSERT INTO usr (user_id, password, balance, token, terminal) values (:user_id, :password, 0, :token, :terminal)",{"user_id":user_id,"password": password,"token":token,"terminal":terminal })
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_user_id(user_id)

        return 200, "ok"

    def unregister(self, user_id: str, password: str):
        user = self.session.execute("SELECT password from usr where user_id=:user_id",
                                        {"user_id": user_id}).fetchone()
        if user == None:
            code, message = error.error_authorization_fail()
            return code, message

        if password != user.password:
            code, message = error.error_authorization_fail()
            return code, message
        self.session.execute("DELETE from usr where user_id='%s'"% (user_id,))
        self.session.commit()

        return 200, "ok"

    def login(self, user_id: str, password: str,terminal:str):
        token = ""
        user = self.session.execute("SELECT password from usr where user_id=:user_id",{"user_id":user_id}).fetchone()
        if user is None or  password != user.password:
            code, message=error.error_authorization_fail()
            return code, message,token
        token = jwt_encode(user_id, terminal)
        self.session.execute(
            "UPDATE usr set token= '%s' , terminal = '%s' where user_id = '%s'"% (token, terminal, user_id) )
        self.session.commit()
        return 200, "ok", token

    def logout(self,user_id: str, token: str):
        try:
            user = self.session.execute("SELECT token from usr where user_id='%s'" % (user_id)).fetchone()
            if user is None:
                return error.error_authorization_fail()
            if user.token != token:
                return error.error_authorization_fail()
            newtoken = ""
            self.session.execute(
                "UPDATE usr SET token = '%s' WHERE user_id='%s'" % (newtoken, user_id))
            self.session.commit()
            return 200, "ok"
        except sqlalchemy.exc.IntegrityError:
            return error.error_authorization_fail()

    def change_password(self, user_id: str,  old_password: str, new_password: str):
        usr = self.session.execute("SELECT password from usr where user_id='%s'"%(user_id,)).fetchone()
        if usr is None  or old_password != usr.password:
            return error.error_authorization_fail()
        self.session.execute(
            "UPDATE usr set password = '%s' where user_id = '%s'"%(new_password,user_id), )
        self.session.commit()
        return 200, "ok"

    def search_author(self, author:str,page:int)-> (int,[dict]):#200,'ok',list[{str,str,str,str,list,bytes}]
        ret=[]
        # select
        # title, author, publisher, book_intro, tags, picture
        # from book where
        # book_id in
        # (select book_id from search_tags where tags='小说' and search_id BETWEEN 20 and 30)
        #已付款
        records=self.session.execute(
            " SELECT title,book.author,publisher,book_intro,tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_author where author='%s' and search_id BETWEEN %d and %d)" % (author,10*page-10,10*page-1)).fetchall()#约对"小说"约0.09s
        if len(records)!=0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author_ = record[1]
                publisher = record[2]
                book_intro =record[3]
                tags = record[4]
                picture = record[5]#为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title, 'author': author_, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags,'picture':base64.b64encode(picture).decode('utf-8')})
            return 200,  ret
        else:
            return 200,  []

    def search_book_intro(self, book_intro:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT title,author,publisher,book.book_intro,tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_book_intro where book_intro='%s' and search_id BETWEEN %d and %d)" % (
            book_intro, 10*page-10,10*page-1)).fetchall()  # 约对"小说"约0.09s
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro_ =record[3]
                tags = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro_,
                     'tags': tags, 'picture':base64.b64encode(picture).decode('utf-8')})
            return 200,  ret
        else:
            return 200,  []
    def search_tags(self, tags:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT title,author,publisher,book_intro,book.tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_tags where tags='%s' and search_id BETWEEN %d and %d)" % (
            tags, 10*page-10,10*page-1)).fetchall()  # 约对"小说"约0.09s
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro =record[3]
                tags_ = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags_, 'picture':base64.b64encode(picture).decode('utf-8')})
            return 200,  ret
        else:
            return 200,  []
    def search_title(self, title:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT book.title,author,publisher,book_intro,tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_title where title='%s' and search_id BETWEEN %d and %d)" % (
            title, 10*page-10,10*page-1)).fetchall()  # 约对"小说"约0.09s
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title_ = record[0]
                author = record[1]
                publisher = record[2]
                book_intro =record[3]
                tags = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title_, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags, 'picture':base64.b64encode(picture).decode('utf-8')})
            return 200,  ret
        else:
            return 200,  []
    def search_author_in_store(self, author:str,store_id:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT title,book.author,publisher,book_intro,tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_author where author='%s') and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d"% (author, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author_ = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title, 'author': author_, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags, 'picture':base64.b64encode(picture).decode('utf-8')})#有byte类会倒是JSON unserializeable 所以需要base64.encode一下 可能会浪费时间
            return 200,  ret
        else:
            return 200, []
    def search_book_intro_in_store(self, book_intro:str,store_id:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT title,author,publisher,book.book_intro,tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_book_intro where book_intro='%s') and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d"% (book_intro, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro_ = record[3]
                tags = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro_,
                     'tags': tags, 'picture':base64.b64encode(picture).decode('utf-8')})
            return 200,  ret
        else:
            return 200,  []
    def search_tags_in_store(self, tags:str,store_id:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT title,author,publisher,book_intro,book.tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_tags where tags='%s') and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d"% (tags, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags_ = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags_, 'picture':base64.b64encode(picture).decode('utf-8')})
            return 200, ret
        else:
            return 200,  []
    def search_title_in_store(self, title:str,store_id:str,page:int)-> (int,[dict]):
        ret = []
        records = self.session.execute(
            " SELECT book.title,author,publisher,book_intro,tags,picture "
            "FROM book WHERE book_id in "
            "(select book_id from search_title where title='%s') and "
            "book_id in (select book_id from store where store_id='%s')"
            "LIMIT 10 OFFSET %d"% (title, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title_ = record[0]
                author = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags = record[4]
                picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
                ret.append(
                    {'title': title_, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags, 'picture':base64.b64encode(picture).decode('utf-8')})
            return 200,  ret
        else:
            return 200,  []

    def search_title_store_id(self, title:str)-> (int,[str]):#前端用  点书名出store_id
        ret = []
        records = self.session.execute(
            " SELECT store_id "
            "FROM store WHERE book_id in "
            "(select book_id from book where title='%s')"% (title)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计

        return 200, records
    def search_pic(self, picture,page=1)-> (int,[(int,int)]):#picture is FileStorage#[(book_id,相似度)]输出前十个
        print(picture.content_type)
        if picture and picture.content_type in ['png','image/png']:
            from .hash import hashTool
            picture=hashTool.HashTool.file_pil(picture)
            photo_list=self.session.execute(
                "SELECT book_id,picture "
                "FROM book where book_id between 260 and 360"
                "LIMIT 100").fetchall()
            thelist=[]
            for i in range(len(photo_list)):
                record = photo_list[i]
                book_id = record[0]
                picture_ = record[1]
                # try:
                picture_=hashTool.HashTool.buffer_pil(picture_)
                thelist.append((picture_,book_id))
                # except OSError:
                #     print(OSError)
            final=hashTool.HashTool.n_smallest(thelist, picture, 10)
            print([i[1] for i in final])
            print([1-hashTool.HashEngine.mean_distance([i],picture)/64 for i in final])
            return 200,[(i[1],1-hashTool.HashEngine.mean_distance([i],picture)/64) for i in final] #[(book_id,相似度)]
        else:
            code, mes = error.error_bad_type()
            return code, mes
    def search_pic_in_store(self, picture,store_id:str,page=1):
        print(picture.content_type)
        if picture and picture.content_type in ['png','image/png']:
            from .hash import hashTool
            picture=hashTool.HashTool.file_pil(picture)
            photo_list=self.session.execute(
                "SELECT book_id,picture "
                "FROM book where book_id in (select book_id from store where store_id='%s')"% (store_id)
                ).fetchall()
            thelist=[]
            for i in range(len(photo_list)):
                record = photo_list[i]
                book_id = record[0]
                picture_ = record[1]
                # try:
                picture_=hashTool.HashTool.buffer_pil(picture_)
                thelist.append((picture_,book_id))
                # except OSError:
                #     print(OSError)
            final=hashTool.HashTool.n_smallest(thelist, picture, 10)
            print([i[1] for i in final])
            print([1-hashTool.HashEngine.mean_distance([i],picture)/64 for i in final])
            return 200,[(i[1],1-hashTool.HashEngine.mean_distance([i],picture)/64) for i in final] #[(book_id,相似度)]
        else:
            code, mes = error.error_bad_type()
            return code, mes

