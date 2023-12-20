import requests
import simplejson
from urllib.parse import urljoin
from fe.access.auth import Auth


class Buyer:
    def __init__(self, url_prefix, user_id, password):
        self.url_prefix = urljoin(url_prefix, "buyer/")
        self.user_id = user_id
        self.password = password
        self.token = ""
        self.terminal = "my terminal"
        self.auth = Auth(url_prefix)
        code, self.token = self.auth.login(self.user_id, self.password, self.terminal)
        assert code == 200

    def new_order(self, store_id: str, book_id_and_count: [(str, int)]) -> (int, str):
        books = []
        for id_count_pair in book_id_and_count:
            books.append({"id": id_count_pair[0], "count": id_count_pair[1]})
        json = {"user_id": self.user_id, "store_id": store_id, "books": books}
        # print(simplejson.dumps(json))
        url = urljoin(self.url_prefix, "new_order")
        headers = {"token": self.token}
        for item in books:
            print(item)
        r = requests.post(url, headers=headers, json=json)
        response_json = r.json()
        print("2929", response_json)
        return r.status_code, response_json.get("order_id")

    def payment(self, order_id: str):
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "order_id": order_id,
        }
        url = urljoin(self.url_prefix, "payment")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code

    def add_funds(self, add_value: str) -> int:
        json = {
            "user_id": self.user_id,
            "password": self.password,
            "add_value": add_value,
        }
        url = urljoin(self.url_prefix, "add_funds")
        headers = {"token": self.token}
        r = requests.post(url, headers=headers, json=json)
        return r.status_code
    
    def search_global(self, key: str, pageIndex: int = 1, pageSize: int = 5) -> int:
        url = urljoin(self.url_prefix, "search_global")+f"?key={key}&pageIndex={str(pageIndex)}&pageSize={str(pageSize)}"
        headers = {"token": self.token}
        print(5858, url)
        r = requests.get(url, headers=headers)      
        return r.status_code
    
    def search_store(self, key: str, store_id: str, pageIndex: int = 1, pageSize: int = 5) -> int:
        url = urljoin(self.url_prefix, "search_store")+f"?key={key}&store_id={store_id}&pageIndex={str(pageIndex)}&pageSize={str(pageSize)}"
        headers = {"token": self.token}
        r = requests.get(url, headers=headers)
        return r.status_code