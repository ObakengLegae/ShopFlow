import pytest
import pandas as pd

from src.shopflow.database.database import Database


@pytest.fixture
def database_instance():
    database = Database(
        host="localhost",
        port=5432,
        database="ecommerce_db",
        user="postgres",
        password="password"
    )
    database.create_tables(database.default_sql)
    return database

@pytest.fixture
def database_connection(database_instance):
    connection = database_instance.connect()
    yield connection
    connection.close()

def test_database_connection(database_connection):
    assert database_connection is not None

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

def test_insert_data_successfully(database_instance, database_connection):
    df_customers = pd.DataFrame({
        "customer_id": ["test01", "test02"],
        "country": ["United Kingdom", "France"],
    })

    database_instance.insert_data(df_customers, "customers")

    df_result = database_instance.fetch_data("./sql/customer_id.sql")

    assert not df_result.empty
    assert len(df_result) == 2
    assert df_result.iloc["country"] == "United Kingdom"
    assert df_result.iloc["country"] == "France"