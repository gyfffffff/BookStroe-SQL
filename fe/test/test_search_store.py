import pytest
from fe.access.buyer import Buyer
from fe.access.seller import Seller
from fe.access.new_buyer import register_new_buyer
from fe.access.new_seller import register_new_seller
import uuid
from fe.test.utils import gen_random_keyword
import random
from fe.access import book
from fe import conf

class TestSearchInStore:
    buyer: Buyer
    seller: Seller

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_search_store_seller_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_search_store_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.seller = register_new_seller(self.seller_id, self.password)
        self.store_id = "test_search_store_id_{}".format(str(uuid.uuid1()))

        code = self.seller.create_store(self.store_id)
        assert code == 200
        book_db = book.BookDB(conf.Use_Large_DB)
        self.books = book_db.get_book_info(0, 18)
        for b in self.books:
            code = self.seller.add_book(self.store_id, 0, b)
            assert code == 200
        

    def test_pageIndex_0(self):
        keyword = gen_random_keyword()  # 生成4-9长度不等的中文短句
        pageIndex = 0
        status = self.buyer.search_store(keyword, self.store_id, pageIndex)
        assert status == 200

    def test_pageSiz_0(self):
        keyword = gen_random_keyword()  # 生成4-9长度不等的中文短句
        pageSize = 0
        status = self.buyer.search_store(keyword, self.store_id, pageSize=pageSize)
        assert status == 200

    def test_page_not_0(self):
        keyword = gen_random_keyword()  # 生成长度不等的中文短句
        pageSize = random.randint(2,6)
        status = self.buyer.search_store(keyword, self.store_id, pageSize=pageSize)
        assert status == 200
    

    def test_invalidparam(self):
        keyword = gen_random_keyword()  # 生成长度不等的中文短句
        pageSize = "2x"
        status = self.buyer.search_store(keyword, self.store_id, pageSize=pageSize)
        assert status == 521
    
    def test_error_store_id_exist(self):
        keyword = gen_random_keyword()  # 生成长度不等的中文短句
        pageIndex = 1
        pageSize = random.randint(2,6)
        status = self.buyer.search_store(keyword, store_id= "fake_store_id", pageIndex=pageIndex, pageSize=pageSize)
        assert status == 513

    def test_error_missing_key(self):
        status = self.buyer.search_store(None, self.store_id, 1, 5)
        assert status == 520
        status = self.buyer.search_store("key", None, 1, 5)
        assert status == 520       
