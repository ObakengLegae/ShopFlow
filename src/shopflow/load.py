import pandas as pd
from numpy.core import records
from psycopg2.extras import execute_values
from sqlalchemy.engine import row

from src.shopflow.extract import extract_data


def load(file_path: str, database_connection):
    processed_data = extract_data(file_path)
    database_connection.connect()

    try:
        load_customers(processed_data, database_connection)

        database_connection.commit()

    except Exception:
        database_connection.rollback()
        raise

    finally:
        database_connection.close()


def load_customers(data: pd.DataFrame, connection):
    customers = data[
        ["customer_id", "country"]
    ].drop_duplicates(subset="customer_id")

    records = [
        (row["customer_id"], row["country"]) for _, row in customers.iterrows()
    ]

    cursor = connection.cursor()

    execute_values(
        cursor,
        """INSERT INTO customers (customer_id, country) VALUES %s""",
        records,
    )

    cursor.close()