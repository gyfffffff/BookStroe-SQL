import pytest
from fe.access.book import Book
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.seller import Seller
import uuid


class TestSearchOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_new_order_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_new_order_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_new_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        self.gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = self.gen_book.gen(
            non_exist_book_id=False, low_stock_level=False
        )
        assert ok
        buy_book_info_list = self.gen_book.buy_book_info_list
        total_price = 0
        self.seller = Seller("http://localhost:5000/", self.seller_id, self.password)
        for item in buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                total_price = total_price + book.price * num
            code = self.seller.add_stock_level(self.seller_id, self.store_id, book.id, num*12)
            assert code==200
        for i in range(12):
            code, order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
            assert code == 200
            
            if i > 3:
                self.buyer.add_funds(total_price)
                assert code == 200
                self.buyer.payment(order_id=order_id)
                assert code == 200
                # if i > 6:
                #     code = self.seller.send(self.seller_id, order_id)
                #     assert code == 200
                #     if i > 9:
                #         code = self.buyer.receive(order_id)
                #         assert code == 200
        yield

    def test_ok_0(self):
        code, order_list = self.buyer.search_order(search_status=0)
        assert code == 200
        assert len(order_list) == 4

    # def test_ok_1(self):
    #     code, order_list = self.buyer.search_order(search_status=1)
    #     assert code == 200
    #     assert len(order_list) == 3

    # def test_ok_2(self):
    #     code, order_list = self.buyer.search_order(search_status=2)
    #     assert code == 200
    #     assert len(order_list) == 3

    # def test_ok_3(self):
    #     code, order_list = self.buyer.search_order(search_status=3)
    #     assert code == 200
    #     assert len(order_list) == 2

    # def test_error_non_exist_user_id(self):
    #     self.buyer.user_id = "non_exist_user_id"
    #     code, order_list = self.buyer.search_order(search_status=0)
    #     assert code != 200

    # def test_search_all(self):
    #     code, order_list = self.buyer.search_order(search_status=-1)
    #     assert code == 200
    #     assert len(order_list) == 12