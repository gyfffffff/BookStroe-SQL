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
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            book_info = json.loads(book_json_str)

            self.cursor.execute(
                "SELECT * FROM book WHERE id = %s", (book_id,)
            )
            if self.cursor.fetchone() is None: 
                self.cursor.execute(
                    'INSERT into book(id, title, publisher, author, original_title, translator, pub_year, pages,currency_unit, binding, isbn, author_intro, book_intro, "content", tags, picture)'
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        book_id, 
                        book_info['title'], 
                        book_info['publisher'], 
                        book_info['author'], 
                        book_info['original_title'], 
                        book_info['translator'], 
                        book_info['pub_year'], 
                        book_info['pages'], 
                        book_info['currency_unit'], 
                        book_info['binding'], 
                        book_info['isbn'], 
                        book_info['author_intro'], 
                        book_info['book_intro'], 
                        book_info['content'], 
                        book_info['tags'], 
                        book_info['pictures'], 
                    ),
                )
                # 分词
                tsvec = cut(book_info)   # 返回一个空格分割的字符串
                self.cursor.execute(
                    'update book set _ts=%s '
                    'where id = %s',
                    (tsvec, book_id)
                )

            self.cursor.execute(
                'INSERT into store(book_id,store_id, stock_level, price) VALUES (%s, %s, %s, %s)',
                (book_id, store_id, stock_level, book_info['price']),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            print(e)
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
                "WHERE store_id = %s AND book_id = %s",
                (add_stock_level, store_id, book_id),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)
            self.cursor.execute(
                'INSERT into bookstore(user_id, store_id) VALUES (%s, %s)',
                (user_id, store_id),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def send(self, user_id:str, order_id:str, token: str):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            self.cursor.execute(
                'SELECT store_id, status FROM "order" WHERE order_id = %s', (order_id,)
            )
            res_order = self.cursor.fetchone()
            if res_order is None:
                return error.error_invalid_order_id(order_id)
            store_id = res_order[0]
            if store_id is None:
                return error.error_invalid_order_id(order_id+" order_id without store_id.")
            status = res_order[1]
            if status != 1:
                return error.error_status(order_id)
            self.cursor.execute(
                'UPDATE "order" SET status = 2 WHERE order_id = %s', (order_id,)
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
    
