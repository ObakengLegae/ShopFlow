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
        """Bulk inserts a Pandas dataframe into the specified table."""
        if df is None or df.empty:
            logger.warning(f"DataFrame for {table_name} is empty. Skipping insert.")
            return

        if not table_name:
            logger.error(f"Invalid table name: {table_name}")
            raise ValueError(f"Invalid table name: {table_name}")

        logger.info(f"Inserting data into table: {table_name}")
        columns = ', '.join(df.columns)
        query = f"INSERT INTO {table_name} ({columns}) VALUES %s ON CONFLICT DO NOTHING"
        data_tuples = list(df.itertuples(index=False, name=None))

        connection = self.connect()
        try:
            with connection:
                with connection.cursor() as cursor:
                    execute_values(cursor, query, data_tuples)
                logger.info(f"Data inserted into {table_name} successfully")
        except Exception as e:
            logger.error(f"Failed to insert data into {table_name}': {e}")
            raise
        finally:
            connection.close()


    def fetch_data(self, query: str, params=None):
        """Executes a SELECT query and returns the results as a Pandas dataframe."""
        self.validate_query(query, "SELECT")
        logger.info("Fetching data...")

        connection = self.connect()

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    return pd.DataFrame(cursor.fetchall(), columns=columns)
                return pd.DataFrame()
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
        finally:
            connection.close()


    def update_data(self, query: str, params=None):
        """Executes Update query."""
        self.validate_query(query, "UPDATE")
        self._execute_write_query(query, params, action="Updating data")


    def delete_data(self, query: str, params=None):
        """Executes Delete query."""
        self.validate_query(query, "DELETE")
        self._execute_write_query(query, params, action="Deleting data")

    def _execute_write_query(self, query: str, params: tuple = None, action: str = None):
        """Helper function removing boilerplate code for UPDATE and DELETE operations."""
        logger.info(f"{action}")
        connection = self.connect()

        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
            logger.info(f"{action} completed successfully")
        except Exception as e:
            logger.error(f"Error during {action.lower()}: {e}")


    def validate_query(self, query: str, expected_command: str):
        """Validates that a query starts with the expected SQL command."""
        if not query or not isinstance(query, str):
            logger.error("Query must be a non-empty string")
            raise ValueError("Query must be a non-empty string")

        clean_query = query.strip().upper()
        if not clean_query.startswith(expected_command):
            logger.error(f"Validation failed. Expected {expected_command} query")
            raise ValueError(f"Expected a {expected_command} query")