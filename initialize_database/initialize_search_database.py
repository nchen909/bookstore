#encoding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint, Text, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker
import psycopg2
from datetime import datetime, time

import jieba.analyse
from jieba import cut_for_search
import re

import time
import datetime
# 连接数据库legend 记得修改这个！！！
#engine = create_engine(Conf.get_sql_conf('local_w'))
engine = create_engine('postgresql://postgres:@localhost:5432/bookstore')

Base = declarative_base()


# 书本表
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


# 搜索标题表
class Search_title(Base):
    __tablename__ = 'search_title'
    search_id = Column(Integer, nullable=False)
    title = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('search_id', 'title'),
        {},
    )


# 搜索标签表
class Search_tags(Base):
    __tablename__ = 'search_tags'
    search_id = Column(Integer, nullable=False)
    tags = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('search_id', 'tags'),
        {},
    )


# 搜索作者表
class Search_author(Base):
    __tablename__ = 'search_author'
    search_id = Column(Integer, nullable=False)
    author = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('search_id', 'author'),
        {},
    )


# 搜索目录表
# class Search_content(Base):
#     __tablename__ = 'search_content'
#     search_id = Column(Integer, nullable=False)
#     content = Column(Text, nullable=False)
#     book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)

#     __table_args__ = (
#         PrimaryKeyConstraint('search_id', 'content'),
#         {},
#     )


# 搜索书本内容表
class Search_book_intro(Base):
    __tablename__ = 'search_book_intro'
    search_id = Column(Integer, nullable=False)
    book_intro = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('search_id', 'book_intro'),
        {},
    )


def insert_tags():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id,tags FROM book;").fetchall()
    for i in row:
        tmp = i.tags.replace("'", "").replace("[", "").replace("]",
                                                               "").split(", ")
        for j in tmp:
            max_num = session.execute(
                "SELECT MAX(search_id) FROM search_tags WHERE tags = '%s';" %
                (j, )).fetchone()
            max_num = max_num[0]
            if max_num == None:
                max_num = 0
            else:
                max_num += 1
            # print(max_num, j, i.book_id)
            session.execute(
                "INSERT into search_tags(search_id, tags, book_id) VALUES (%d, '%s', %d)"
                % (max_num, j, int(i.book_id)))
    session.commit()


def insert_author():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id, author FROM book;").fetchall()
    for i in row:
        tmp = i.author
        if tmp == None:
            j = '作者不详'
            max_num = session.execute(
                "SELECT MAX(search_id) FROM search_author WHERE author = '%s';"
                % (j, )).fetchone()
            max_num = max_num[0]
            if max_num == None:
                max_num = 0
            else:
                max_num += 1
            # print(max_num, j, i.book_id)
            session.execute(
                "INSERT into search_author(search_id, author, book_id) VALUES (%d, '%s', %d)"
                % (max_num, j, int(i.book_id)))

        else:
            tmp = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', tmp)
            tmp = re.sub(r'[^\w\s]', '', tmp)
            length = len(tmp)
            for k in range(1, length + 1):
                if tmp[k - 1] == '':
                    continue
                j = tmp[:k]
                max_num = session.execute(
                    "SELECT MAX(search_id) FROM search_author WHERE author = '%s';"
                    % (j, )).fetchone()
                max_num = max_num[0]
                if max_num == None:
                    max_num = 0
                else:
                    max_num += 1
                # print(max_num, j, i.book_id)
                session.execute(
                    "INSERT into search_author(search_id, author, book_id) VALUES (%d, '%s', %d)"
                    % (max_num, j, int(i.book_id)))
    session.commit()


def insert_title():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id, title FROM book;").fetchall()
    for i in row:
        tmp = i.title
        # print(tmp)
        tmp = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', tmp)
        tmp = re.sub(r'[^\w\s]', '', tmp)
        # 处理空标题
        if len(tmp) == 0:
            continue

        # 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
        seg_list = cut_for_search(tmp)
        sig_list = []
        tag = 0
        for k in seg_list:
            sig_list.append(k)
            if k == tmp:
                tag = 1
        if tag == 0:
            sig_list.append(tmp)

        for j in sig_list:
            if j == "" or j == " ":
                continue
            max_num = session.execute(
                "SELECT MAX(search_id) FROM search_title WHERE title = '%s';" %
                (j, )).fetchone()
            max_num = max_num[0]
            if max_num == None:
                max_num = 0
            else:
                max_num += 1
            # print(max_num, j, i.book_id)
            session.execute(
                "INSERT into search_title(search_id, title, book_id) VALUES (%d, '%s', %d)"
                % (max_num, j, int(i.book_id)))
    session.commit()


# def insert_content():
#     DBSession = sessionmaker(bind=engine)
#     session = DBSession()
#     Base.metadata.create_all(engine)
#     row = session.execute("SELECT book_id, content FROM book;").fetchall()
#     for i in row:
#         tmp = i.content
#         if tmp != None:
#             tmp = tmp.split("\n")
#             for j in tmp:
#                 j = re.sub(r'第.*\s\t?', '', j)
#                 j = re.sub(r'[^\w\s]', '', j)
#                 if j == '· · · · · ·     (' or j == '……':
#                     break
#                 if j == "":
#                     continue
#                 max_num = session.execute(
#                     "SELECT MAX(search_id) FROM search_content WHERE content = '%s';"
#                     % (j, )).fetchone()
#                 max_num = max_num[0]
#                 if max_num == None:
#                     max_num = 0
#                 else:
#                     max_num += 1
#                 # print(max_num, j, i.book_id)
#                 session.execute(
#                     "INSERT into search_content(search_id, content, book_id) VALUES (%d, '%s', %d)"
#                     % (max_num, j, int(i.book_id)))
#     session.commit()


def insert_book_intro():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id, book_intro FROM book;").fetchall()
    for i in row:
        tmp = i.book_intro
        if tmp != None:
            # print(tmp)
            # 采用textrank进行分词
            keywords_textrank = jieba.analyse.textrank(tmp)
            # print(keywords_textrank)
            # keywords_tfidf = jieba.analyse.extract_tags(tmp)
            # print(keywords_tfidf)
            for j in keywords_textrank:
                max_num = session.execute(
                    "SELECT MAX(search_id) FROM search_book_intro WHERE book_intro = '%s';"
                    % (j, )).fetchone()
                max_num = max_num[0]
                if max_num == None:
                    max_num = 0
                else:
                    max_num += 1
                # print(max_num, j, i.book_id)
                session.execute(
                    "INSERT into search_book_intro(search_id, book_intro, book_id) VALUES (%d, '%s', %d)"
                    % (max_num, j, int(i.book_id)))
    session.commit()


def init():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)
    # 提交即保存到数据库
    session.commit()
    # 关闭session
    session.close()


if __name__ == "__main__":
    # 创建数据库
    init()
    # 插入表
    start = datetime.datetime.now()
    insert_tags()
    insert_author()
    insert_title()
    insert_book_intro()
    end = datetime.datetime.now()
    print("spend {} sec".format((end - start).seconds))