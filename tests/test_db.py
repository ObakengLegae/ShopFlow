from datetime import date

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

def test_fetch_data(database_instance):
    df_customers = pd.DataFrame({
        "customer_id": ["f_cust01", "f_cust02"],
        "country": ["Spain", "Italy"],
    })
    database_instance.insert_data(df_customers, "customers")

    df_all = database_instance.fetch_data("SELECT * FROM customers WHERE customer_id LIKE 'f_cust%';")
    assert len(df_all) == 2

    df_param = database_instance.fetch_data("SELECT * FROM customers WHERE country = %s;", ("Spain",))
    assert len(df_param) == 1
    assert df_param.iloc[0]["country"] == "Spain"


def test_insert_customers_successfully(database_instance):
    df_customers = pd.DataFrame({
        "customer_id": ["test01", "test02"],
        "country": ["United Kingdom", "France"],
    })

    database_instance.insert_data(df_customers, "customers")

    df_result = database_instance.fetch_data("SELECT * FROM customers WHERE customer_id IN ('test01', 'test02');")

    assert not df_result.empty
    assert len(df_result) == 2

    customer_ids = df_result["customer_id"].to_list()
    countries = df_result["country"].to_list()

    assert "test01" in customer_ids
    assert "test02" in customer_ids
    assert "United Kingdom" in countries
    assert "France" in countries

def test_insert_products_successfully(database_instance):
    df_products = pd.DataFrame({
        "stock_code": ["P001", "P002"],
        "description": ["Test Product 1", "Test Product 2"],
    })

    database_instance.insert_data(df_products, "products")

    df_result = database_instance.fetch_data("SELECT * FROM products WHERE stock_code IN ('P001', 'P002');")

    assert not df_result.empty
    assert len(df_result) == 2

    stock_codes = df_result["stock_code"].to_list()
    descriptions = df_result["description"].to_list()

    assert "P001" in stock_codes
    assert "P002" in stock_codes
    assert "Test Product 1" in descriptions
    assert "Test Product 2" in descriptions

def test_insert_dates_successfully(database_instance):

    df_dates = pd.DataFrame({
        "date_id": [20230101, 20230102],
        "full_date": [date(2023, 1, 1), date(2023, 1, 2)],
        "year": [2023, 2023],
        "month": [1, 1],
        "day": [1, 2],
        "quarter": [1, 1],
        "day_of_week": ["Sunday", "Monday"]
    })

    database_instance.insert_data(df_dates, "dates")

    df_result = database_instance.fetch_data("SELECT * FROM dates WHERE date_id IN (20230101, 20230102);")

    assert not df_result.empty
    assert len(df_result) == 2

    date_ids = df_result["date_id"].to_list()
    years = df_result["year"].to_list()

    assert 20230101 in date_ids
    assert 20230102 in date_ids
    assert 2023 in years