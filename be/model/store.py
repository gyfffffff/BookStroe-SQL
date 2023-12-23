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
