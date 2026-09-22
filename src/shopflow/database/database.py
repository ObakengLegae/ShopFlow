import psycopg2

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