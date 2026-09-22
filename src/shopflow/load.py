import pandas as pd
from numpy.core import records
from psycopg2.extras import execute_values
from sqlalchemy.engine import row


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