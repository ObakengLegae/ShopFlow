import pytest
from src.shopflow.database.database import Database


@pytest.fixture
def database_connection():
    database = Database(
        host="localhost",
        port=5432,
        database="ecommerce_db",
        user="postgres",
        password="password"
    )
    connection = database.connect()
    database.create_tables(database.default_sql)
    return connection


def test_database_connection(database_connection):
    assert database_connection is not None
    database_connection.close()

def test_tables_created_successfully(database_connection):
    cursor = database_connection.cursor()
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public';
    """)

    tables = cursor.fetchall()

    expected_tables = ["customers", "products", "dates", "sales"]
    table_names = [table[0] for table in tables]

    for name in expected_tables:
        assert name in table_names