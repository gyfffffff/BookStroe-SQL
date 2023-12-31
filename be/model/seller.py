import psycopg2
from be.model import error
from be.model import db_conn, user
import json
from be.model.utils import cut


class Seller(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)
        self.User = user.User()

    def add_book(
        self,
        user_id: str,
        store_id: str,
        book_id: str,
        book_json_str: str,
        stock_level: int,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            # if not self.store_id_exist(store_id):
            #     return error.error_non_exist_store_id(store_id)
            # if self.book_id_exist(store_id, book_id):
            #     return error.error_exist_book_id(book_id)

            book_info = json.loads(book_json_str)

            self.cursor.execute("SELECT * FROM book WHERE id = %s", (book_id,))
            if self.cursor.fetchone() is None:
                tsvec = cut(book_info)  # 返回一个空格分割的字符串
                self.cursor.execute(
                    'INSERT into book(id, title, publisher, author, original_title, translator, pub_year, pages,currency_unit, binding, isbn, author_intro, book_intro, "content", tags, picture, _ts)'
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        book_id,
                        book_info["title"],
                        book_info["publisher"],
                        book_info["author"],
                        book_info["original_title"],
                        book_info["translator"],
                        book_info["pub_year"],
                        book_info["pages"],
                        book_info["currency_unit"],
                        book_info["binding"],
                        book_info["isbn"],
                        book_info["author_intro"],
                        book_info["book_intro"],
                        book_info["content"],
                        book_info["tags"],
                        book_info["pictures"],
                        tsvec,
                    ),
                )

            self.cursor.execute(
                "INSERT into store(book_id,store_id, stock_level, price) VALUES (%s, %s, %s, %s)",
                (book_id, store_id, stock_level, book_info["price"]),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return error.error_database(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def add_stock_level(
        self, user_id: str, store_id: str, book_id: str, add_stock_level: int
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            self.cursor.execute(
                "UPDATE store SET stock_level = stock_level + %s "
                "WHERE book_id = %s AND store_id = %s",
                (add_stock_level, book_id, store_id),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return error.error_database(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str, token: str) -> (int, str):
        try:
            code, message = self.User.check_token(user_id, token)
            if code != 200:
                return error.error_and_message(code, message)
            # if self.store_id_exist(store_id):
            #     return error.error_exist_store_id(store_id)
            self.cursor.execute(
                "INSERT into bookstore(store_id, user_id) VALUES (%s, %s)",
                (store_id, user_id),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return error.error_database(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def send(self, user_id: str, order_id: str, token: str):
        try:
            code, message = self.User.check_token(user_id, token)
            if code != 200:
                return error.error_and_message(code, message)
            self.cursor.execute(
                'SELECT status FROM "order" WHERE order_id = %s', (order_id,)
            )
            res_order = self.cursor.fetchone()
            if res_order is None:
                return error.error_invalid_order_id(order_id)
            # store_id = res_order[0]
            status = res_order[0]
            if status != 1:
                return error.error_status(order_id)
            self.cursor.execute(
                'UPDATE "order" SET status = 2 WHERE order_id = %s', (order_id,)
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return error.error_database(e)
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
