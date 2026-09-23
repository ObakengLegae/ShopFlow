import os
import logging

import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class Database:
    """Manages PostgreSQL database connection"""
    def __init__(self):
        required_variables = ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        missing_variables = [var for var in required_variables if not os.getenv(var)]
        if missing_variables:
            logger.error(f"Missing required database environment variables: {';'.join(missing_variables)}")
            raise EnvironmentError(f"Missing required database environment variables: {';'.join(missing_variables)}")

        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_NAME")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")

        self.default_sql = "./sql/schema.sql"

    def connect(self):
        """Connects to PostgreSQL database and returns connection."""
        try:
            return psycopg2.connect(
            host = self.host,
            port = self.port,
            database = self.database,
            user = self.user,
            password = self.password
        )
        except psycopg2.OperationalError as e:
            logger.error(f"Failed to connect to PostgreSQL database: {e}")
            raise

    def create_tables(self, sql_file: str):
        """Executes an SQL file to create database tables."""
        if not os.path.exists(sql_file):
            logger.error(f"SQL file not found at path: {sql_file}")
            raise FileNotFoundError(f"Schema file missing: {sql_file}")

        logger.info(f"Creating tables...")
        connection = self.connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    with open(sql_file, "r") as file:
                        sql = file.read()
                    cursor.execute(sql)
            logger.info("Tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            raise
        finally:
            connection.close()

    def insert_data(self, df: pd.DataFrame, table_name: str):
        connection = self.connect()
        print("Inserting data...")
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
        print("Data inserted")


    def fetch_data(self, query: str, params=None):
        connection = self.connect()
        print("Fetching data...")
        cursor = connection.cursor()

        self.validate_query(query, "SELECT")
        try:
            cursor.execute(query, params)
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                return pd.DataFrame(cursor.fetchall(), columns=columns)
            return pd.DataFrame()
        finally:
            cursor.close()
            connection.close()


    def update_data(self, query: str, params=None):
        connection = self.connect()
        cursor = connection.cursor()

        self.validate_query(query, "UPDATE")

        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()


    def delete_data(self, query: str, params=None):
        connection = self.connect()
        cursor = connection.cursor()

        self.validate_query(query, "DELETE")

        try:
            cursor.execute(query, params)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            cursor.close()
            connection.close()

    def validate_query(self, query: str, expected_command: str):
        query = query.strip().upper()

        if not query.startswith(expected_command):
            raise ValueError(f"Expected a {expected_command} query")