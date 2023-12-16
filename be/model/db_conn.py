from be.model import store


class DBConn:
    def __init__(self):
        self.database = store.get_db()
        self.cursor = store.get_db_conn()

    def user_id_exist(self, user_id):
        cursor = self.cursor.execute(
            "SELECT user_id FROM 'user' WHERE user_id = %s;", (user_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        cursor = self.cursor.execute(
            "SELECT book_id FROM store WHERE store_id = %s AND book_id = %s;",
            (store_id, book_id),
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        cursor = self.cursor.execute(
            "SELECT store_id FROM user_store WHERE store_id = %s;", (store_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return False
        else:
            return True
