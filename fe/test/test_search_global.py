import pytest
from fe.access.buyer import Buyer
from fe.access.new_buyer import register_new_buyer
import uuid
from fe.test.utils import gen_random_keyword
import random

class TestSearchGlobal:
    buyer: Buyer

    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_search_in_store_seller_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_search_in_store_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        

    def test_page_0(self):
        keyword = gen_random_keyword()  # 生成4-9长度不等的中文短句
        pageIndex = 0
        status= self.buyer.search_global(keyword, pageIndex=pageIndex)
        assert status == 200

    def test_page_not_0(self):
        keyword = gen_random_keyword()  # 生成4-9长度不等的中文短句
        pageIndex = random.randint(2,6)
        status = self.buyer.search_global(keyword, pageIndex=pageIndex)
        assert status == 200
    
    def test_page_none(self):
        keyword = gen_random_keyword()  # 生成4-9长度不等的中文短句
        pageSize = None
        status = self.buyer.search_global(keyword, pageSize=pageSize)
        assert status == 200

    def test_ok(self):
        keyword = gen_random_keyword()  # 生成4-9长度不等的中文短句
        pageIndex = random.randint(2,6)
        pageSize = random.randint(2,6)
        status = self.buyer.search_global(keyword, pageIndex=pageIndex, pageSize=pageSize)
        assert status == 200

    def test_error(self):
        keyword = gen_random_keyword()+'\n'  # 生成4-9长度不等的中文短句
        pageIndex = random.randint(2,6)
        pageSize = random.randint(2,6)
        status = self.buyer.search_global(keyword, pageIndex=pageIndex, pageSize=pageSize)
        assert status == 530

    def test_error_arg(self):
        keyword = gen_random_keyword()
        pageIndex = str(random.randint(2,6))+"x"
        pageSize = random.randint(2,6)
        status = self.buyer.search_global(keyword, pageIndex=pageIndex, pageSize=pageSize)  
        assert status != 200