import logging
import psycopg2


class Store:
    database: str

    def __init__(self):
        self.database = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="070327",
            database="be",
            port="5432",
        )
        self.init_tables()

    def init_tables(self):
        try:
            cursor = self.database.cursor()
            cursor.execute(   # 判断数据库是否为空
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'book'
                );
                """
            )
            table_exists = cursor.fetchone()[0]

            if not table_exists:
                with open('be/model/create_be.sql', 'r', encoding="utf-8") as file:
                    sql_commands = file.read()
                cursor.execute(sql_commands)

            # cursor.execute(
            #     "CREATE TABLE IF NOT EXISTS bookstore("
            #     "store_id TEXT, user_id TEXT, PRIMARY KEY(store_id));"
            # )

            # cursor.execute(
            #     "CREATE TABLE IF NOT EXISTS book( "
            #     "id TEXT, title TEXT, publisher TEXT, author TEXT,"
            #     "original_title TEXT, translator TEXT, pub_year TEXT,pages INTEGER,"
            #     "currency_unit TEXT,binding TEXT,isbn TEXT,author_intro TEXT,book_intro text,"
            #     "content TEXT,tags TEXT,picture TEXT, _ts tsvector, "
            #     "PRIMARY KEY(id));"
            # )
            # cursor.execute(
            #     "CREATE INDEX IF NOT EXISTS book_ts_idx ON book USING gin(_ts);"
            # )

            # cursor.execute(
            #     "CREATE TABLE IF NOT EXISTS store( "
            #     "book_id TEXT, store_id TEXT, stock_level INTEGER, price INTEGER, "
            #     "PRIMARY KEY(book_id, store_id))"
            # )

            # cursor.execute(
            #     """CREATE TABLE IF NOT EXISTS "order"( 
            #     order_id TEXT, user_id TEXT, store_id TEXT, create_time DATE, pay_ddl DATE,status INTEGER, price INTEGER,  
            #     PRIMARY KEY(order_id));"""
            # )

            # cursor.execute(
            #     "CREATE TABLE IF NOT EXISTS order_book( "
            #     "order_id TEXT, book_id TEXT, count INTEGER, "
            #     "PRIMARY KEY(order_id, book_id))"
            # )

            # cursor.execute(
            #     'ALTER TABLE order_book ADD CONSTRAINT order_book_fk FOREIGN KEY (book_id) REFERENCES book(id);'
            # )

            # cursor.execute(
            #     'ALTER TABLE order_book ADD CONSTRAINT order_book_fk2 FOREIGN KEY (order_id) REFERENCES public."order"(order_id) ON DELETE CASCADE ON UPDATE CASCADE;'
            # )

            self.database.commit()
        except Exception as e:
            logging.error(e)
            self.database.rollback()

    def get_db_conn(self):
        return self.database.cursor()

    def get_db(self):
        return self.database


database_instance: Store = None


def init_database():
    global database_instance
    database_instance = Store()


def get_db_conn():
    global database_instance
    return database_instance.get_db_conn()


def get_db():
    global database_instance
    return database_instance.get_db()
