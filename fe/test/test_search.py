import time

import pytest

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