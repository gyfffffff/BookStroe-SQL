import pytest
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
from fe.access.buyer import Buyer
from fe.access.seller import Seller
import uuid
from fe.test.gen_book_data import GenBook

class TestSend:
    seller_id: str
    store_id: str
    buyer_id: str
    password: str
    buy_book_info_list: [Book]
    total_price: int
    order_id: str
    buyer: Buyer
    seller: Seller
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_send_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_send_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_send_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id

        # self.seller = register_new_seller(self.seller_id, self.password)
        
        self.buyer = register_new_buyer(self.buyer_id, self.password)

        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(
            non_exist_book_id=False, low_stock_level=False, max_book_count=5
        )
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
        assert code == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        self.buyer.add_funds(self.total_price)
        assert code == 200
        self.buyer.payment(order_id=self.order_id)
        assert code == 200
        yield

    def test_ok(self):
        self.seller = Seller("http://localhost:5000/", self.seller_id, self.password)
        code = self.seller.send(self.seller_id, self.order_id)
        assert code == 200
    
    def test_error_non_exist_user_id(self):
        self.seller = Seller("http://localhost:5000/", self.seller_id, self.password)
        code = self.seller.send(self.seller_id + "_x", self.order_id)
        assert code != 200
    
    def error_invalid_order_id(self):
        self.seller = Seller("http://localhost:5000/", self.seller_id, self.password)
        code = self.seller.send(self.seller_id, self.order_id + "_x")
        assert code != 200

    def error_status(self):
        self.seller = Seller("http://localhost:5000/", self.seller_id, self.password)
        code = self.seller.send(self.seller_id, self.order_id)
        assert code == 200
        code = self.seller.send(self.seller_id, self.order_id)
        assert code != 200
    
    
        