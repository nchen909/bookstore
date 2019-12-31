import time

import pytest
from fe.access.new_seller import register_new_seller
from fe.access.book import Book
from fe.access import book
from fe.access import auth
from fe import conf
import uuid
import random
class TestSearch:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.auth = auth.Auth(conf.URL)
        self.author = "test_author_{}".format(str(uuid.uuid1()))
        self.book_intro = "test_book_intro_{}".format(str(uuid.uuid1()))
        self.tags = random.choice(["小说","励志"])
        self.title = random.choice(["很","在"])
        self.store_id = "test_store_id_{}".format(str(uuid.uuid1()))
        self.page = random.randint(1,2)

        yield

    def test_search(self):
        assert self.auth.search_author(self.author, self.page) == 200
        assert self.auth.search_book_intro(self.book_intro, self.page) == 200
        assert self.auth.search_tags(self.tags, self.page) == 200
        assert self.auth.search_title(self.title, self.page) == 200
        assert self.auth.search_author_in_store(self.author, self.store_id,self.page) == 200
        assert self.auth.search_book_intro_in_store(self.book_intro, self.store_id,self.page) == 200
        assert self.auth.search_tags_in_store(self.title, self.store_id,self.page) == 200
        assert self.auth.search_title_in_store(self.tags, self.store_id,self.page) == 200


    def test_search2(self):
        self.store_id = "test_add_books_store_id_b288ead4-212a-11ea-b13e-acde48001122"
        assert self.auth.search_author("西尔维娅娜萨", 1) == 200
        assert self.auth.search_book_intro("再现", 1) == 200
        assert self.auth.search_tags("传记", 1) == 200
        assert self.auth.search_title("美丽", 1) == 200
        assert self.auth.search_author_in_store("西尔维娅娜萨", self.store_id, 1) == 200
        assert self.auth.search_book_intro_in_store("再现", self.store_id, 1) == 200
        assert self.auth.search_tags_in_store("传记", self.store_id, 1) == 200
        assert self.auth.search_title_in_store("美丽", self.store_id, 1) == 200

