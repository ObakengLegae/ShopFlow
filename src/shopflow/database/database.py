import psycopg2
import pandas as pd
from psycopg2.extras import execute_values


class Database:

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.default_sql = "./sql/schema.sql"

    def connect(self):
        return psycopg2.connect(
            host = self.host,
            port = self.port,
            database = self.database,
            user = self.user,
            password = self.password
        )

    def create_tables(self, sql_file):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            with open(sql_file, "r") as file:
                sql = file.read()

            cursor.execute(sql)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

#Todo: Add some validation logic against empty frames and table names
    def insert_data(self, df: pd.DataFrame, table_name: str):
        connection = self.connect()
        cursor = connection.cursor()

        columns = ', '.join(df.columns)
        query = f"INSERT INTO {table_name} ({columns}) VALUES %s"

        data_tuples = list(df.itertuples(index=False, name=None))

        try:
            execute_values(cursor, query, data_tuples)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    def fetch_data(self, query, params=None):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(cursor.fetchall(), columns=columns)
            return pd.DataFrame()
        finally:
            cursor.close()
            connection.close()


    def update_data(self, query, params=None):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    def delete_data(self, query, params=None):
        connection = self.connect()
        cursor = connection.cursor()

        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()