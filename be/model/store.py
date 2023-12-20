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
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS "user" (
                user_id TEXT PRIMARY KEY,  password TEXT NOT NULL, 
                balance INTEGER NOT NULL, token TEXT, terminal TEXT);
                """
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS bookstore("
                "user_id TEXT, store_id TEXT, PRIMARY KEY(user_id, store_id));"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS book( "
                "id TEXT, title TEXT, publisher TEXT, author TEXT,"
                "original_title TEXT, translator TEXT, pub_year TEXT,pages INTEGER,"
                "currency_unit TEXT,binding TEXT,isbn TEXT,author_intro TEXT,book_intro text,"
                "content TEXT,tags TEXT,picture TEXT, _ts tsvector, "
                "PRIMARY KEY(book_id));"
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS store( "
                "book_id TEXT, store_id TEXT, stock_level INTEGER, price INTEGER, "
                "PRIMARY KEY(book_id, store_id))"
            )

            cursor.execute(
                """CREATE TABLE IF NOT EXISTS "order"( 
                order_id TEXT, user_id TEXT, store_id TEXT, create_time DATE, pay_ddl DATE,status INTEGER, price INTEGER,  
                PRIMARY KEY(order_id));"""
            )

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS order_book( "
                "order_id TEXT, book_id TEXT, count INTEGER, "
                "PRIMARY KEY(order_id, book_id))"
            )

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
