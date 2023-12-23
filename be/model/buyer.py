import psycopg2
import uuid
import logging
from be.model import db_conn, user
from be.model import error
from fe.test.utils import cut_word


class Buyer(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)
        self.User = user.User()

    def get_current_time(self):
        cursor = self.cursor.execute("SELECT CURRENT_TIMESTAMP")
        row = self.cursor.fetchone()
        return row[0]

    def get_time_after_30_min(self):
        self.cursor.execute("SELECT CURRENT_TIMESTAMP + INTERVAL '30 minutes'")
        row = self.cursor.fetchone()
        return row[0]

    def new_order(
        self, user_id: str, store_id: str, id_and_count: [(str, int)]
    ) -> (int, str, str):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id,)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id,)
            uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            order_price = 0
            create_time = self.get_current_time()
            pay_ddl = self.get_time_after_30_min()
            status = 0  # 0: 未支付, 1: 已支付未发货, 2: 已发货未收货, 3: 已收货, 4: 已取消
            self.cursor.execute(
                'INSERT INTO "order"(order_id, user_id, store_id, create_time, pay_ddl, status, price) '
                "VALUES(%s, %s, %s, %s, %s, %s, %s);",
                (uid, user_id, store_id, create_time, pay_ddl, status, order_price),
            )
            for book_id, count in id_and_count:
                # 拿到(stock_level, price)-->store, 就不需要解析json了
                cursor = self.cursor.execute(
                    "SELECT stock_level, price FROM store "
                    "WHERE store_id = %s AND book_id = %s;",
                    (store_id, book_id),
                )
                row = self.cursor.fetchone()
                if row is None:
                    return error.error_non_exist_book_id(book_id) + (order_id,)

                stock_level, price = row[0], row[1]

                if stock_level < count:
                    return error.error_stock_level_low(book_id) + (order_id,)

                cursor = self.cursor.execute(
                    "UPDATE store set stock_level = stock_level - %s "
                    "WHERE store_id = %s and book_id = %s and stock_level >= %s; ",
                    (count, store_id, book_id, count),
                )
                order_price += count * price
                self.cursor.execute(
                    "INSERT INTO order_book(order_id, book_id, count) "
                    "VALUES(%s, %s, %s);",
                    (uid, book_id, count),
                )
            self.cursor.execute(
                'UPDATE "order" set price = %s WHERE order_id = %s',
                (order_price, uid),
            )

            self.database.commit()
            order_id = uid
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""

        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        conn = self.cursor
        try:
            conn.execute(
                'SELECT order_id, user_id, store_id, price FROM "order" WHERE order_id = %s',
                (order_id,),
            )
            row = self.cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)

            order_id = row[0]
            buyer_id = row[1]
            store_id = row[2]
            total_price = row[3]

            if buyer_id != user_id:
                return error.error_authorization_fail()

            conn.execute(
                'SELECT balance, password FROM "user" WHERE user_id = %s;', (buyer_id,)
            )
            row = self.cursor.fetchone()
            balance = row[0]
            if password != row[1]:
                return error.error_authorization_fail()

            conn.execute(
                "SELECT user_id FROM bookstore WHERE store_id = %s;",
                (store_id,),
            )
            row = self.cursor.fetchone()

            seller_id = row[0]

            if balance < total_price:
                return error.error_not_sufficient_funds(order_id)

            conn.execute(
                'UPDATE "user" set balance = balance - %s '
                "WHERE user_id = %s AND balance >= %s",
                (total_price, buyer_id, total_price),
            )

            conn.execute(
                'UPDATE "user" set balance = balance + %s WHERE user_id = %s',
                (total_price, seller_id),
            )

            conn.execute(
                'UPDATE "order" set status = 1 WHERE order_id = %s', (order_id,)
            )

            self.database.commit()

        except psycopg2.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        try:
            cursor = self.cursor.execute(
                'SELECT password  from "user" where user_id=%s', (user_id,)
            )
            row = self.cursor.fetchone()
            if row is None:
                return error.error_authorization_fail()

            if row[0] != password:
                return error.error_authorization_fail()

            cursor = self.cursor.execute(
                'UPDATE "user" SET balance = balance + %s WHERE user_id = %s',
                (add_value, user_id),
            )

            self.database.commit()
        except psycopg2.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))

        return 200, "ok"

    def search_global(self, key, pageIndex=1, pageSize=5):
        try:
            if not key:
                return error.error_missing_args("key")
            try:
                if pageIndex is None or int(pageIndex) < 1:
                    pageIndex = 1
                if pageSize is None or int(pageSize) < 1:
                    pageSize = 5
            except:
                return error.error_args("invalid pageIndex or pageSize")
            key = cut_word(key)
            key = " | ".join(key)
            offset = (int(pageIndex) - 1) * int(pageSize)
            self.cursor.execute(
                "select * from book where _ts @@ %s::tsquery LIMIT %s OFFSET %s",
                (key, pageSize, offset),
            )
            result = self.cursor.fetchall()
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", result

    def search_store(self, key, store_id, pageIndex=1, pageSize=5):
        try:
            if not key:
                return error.error_missing_args("key") + ("",)
            if not store_id:
                return error.error_missing_args("store_id") + ("",)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + ("",)
            try:
                if pageIndex is None or int(pageIndex) < 1:
                    pageIndex = 1
                if pageSize is None or int(pageSize) < 1:
                    pageSize = 5
            except:
                return error.error_args("invalid pageIndex or pageSize") + ("",)
            key = cut_word(key)
            key = " | ".join(key)
            offset = (int(pageIndex) - 1) * int(pageSize)
            self.cursor.execute(
                "select * from book where _ts @@ %s::tsquery and id in (select book_id from store where store_id = %s) LIMIT %s OFFSET %s;",
                (key, store_id, pageSize, offset),
            )
            result = self.cursor.fetchall()
            self.database.commit()
        except psycopg2.Error as e:
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", result

    def receive(self, buyer_id, order_id, token):
        code, message = self.User.check_token(buyer_id, token)
        if code != 200:
            return error.error_and_message(code, message)
        try:
            self.cursor.execute(
                'SELECT status, user_id FROM "order" WHERE order_id = %s', (order_id,)
            )
            row = self.cursor.fetchone()
            if row is None:
                return error.error_invalid_order_id(order_id)
            status = row[0]
            if status != 2:
                return error.error_invalid_order_id(order_id)
            user_id = row[1]
            self.cursor.execute(
                'UPDATE "order" SET status = 3 WHERE order_id = %s', (order_id,)
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    def search_order(self, user_id, search_state):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + ("",)
            if search_state == -1:
                self.cursor.execute(
                    'SELECT * FROM "order" WHERE user_id = %s', (user_id,)
                )
            else:
                self.cursor.execute(
                    'SELECT * FROM "order" WHERE user_id = %s and status = %s',
                    (user_id, search_state),
                )
            result = self.cursor.fetchall()
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", result

    def delete_order(
        self,
        user_id,
        order_id,
    ):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            self.cursor.execute(
                'select status, price, store_id from "order" where order_id = %s;',
                (order_id,),
            )
            res = self.cursor.fetchone()
            state = int(res[0])
            total_price = res[1]
            store_id = res[2]
            if 1 <= state <= 3:  # 已付款
                self.cursor.execute(
                    'UPDATE "user" set balance = balance + %s WHERE user_id = %s;',
                    (total_price, user_id),
                )
            elif state == 4:
                return 200, "ok"
            self.cursor.execute(
                "select book_id,count from order_book where order_id = %s;", (order_id,)
            )
            book_count = self.cursor.fetchall()
            for book_id, count in book_count:
                self.cursor.execute(
                    "update store set stock_level = stock_level + %s where book_id = %s and store_id = %s;",
                    (count, book_id, store_id),
                )
            self.cursor.execute(
                'update "order" set status = 4 WHERE order_id = %s;', (order_id,)
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            self.database.rollback()
            return 530, "{}".format(str(e))
        return 200, "ok"

    def delete_order_time(self):
        # 删除超时未支付订单
        try:
            now = self.get_current_time()
            self.cursor.execute(
                'update "order" set status = 4 WHERE status = 0 and pay_ddl < %s;',
                (now,),
            )
            self.database.commit()
        except psycopg2.Error as e:
            self.database.rollback()
            return 528, "{}".format(str(e))
        except BaseException as e:
            self.database.rollback()
            return 530, "{}".format(str(e))
