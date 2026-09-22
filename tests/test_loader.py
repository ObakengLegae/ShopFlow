import pytest
import pandas as pd

from src.shopflow.database.database import Database
from src.shopflow.extractor import Extractor
from src.shopflow.loader import Loader

sample_data_path = "./tests/resources/sample_data.csv"
@pytest.fixture
def database_instance():
    database = Database()
    database.create_tables(database.default_sql)
    try:
        database.delete_data("DELETE FROM sales; DELETE FROM customers; DELETE FROM products; DELETE FROM dates")
    except Exception:
        pass

    yield database

    try:
        database.delete_data("DELETE FROM sales; DELETE FROM customers; DELETE FROM products; DELETE FROM dates")

    except Exception:
        pass

@pytest.fixture
def loader_instance(database_instance):
    return Loader(database_instance)

@pytest.fixture
def sample_data():
    extractor = Extractor()
    data = extractor.extract_data(sample_data_path)
    return data

def test_load_customers(database_instance, loader_instance, sample_data):
    loader_instance.load_customers(sample_data)

    df_result = database_instance.fetch_data("SELECT * FROM customers WHERE customer_id IN ('17850', '13047', '12583');")

    assert not df_result.empty
    assert len(df_result) == 3
    assert set(df_result["customer_id"]) == {"17850", "13047", "12583"}
    assert set(df_result["country"]) == {"United Kingdom", "France"}

def test_load_products(database_instance, loader_instance, sample_data):
    loader_instance.load_products(sample_data)

    df_result = database_instance.fetch_data("SELECT * FROM products WHERE stock_code IN ('22633', '22632', '84879', '22728')")

    assert not df_result.empty
    assert len(df_result) == 4
    assert set(df_result["stock_code"]) == {"22633", "22632", "84879", "22728"}

def test_load_dates(database_instance, loader_instance, sample_data):
    loader_instance.load_dates(sample_data)

    df_result = database_instance.fetch_data("SELECT * FROM dates WHERE date_id = 20101201;")

    assert not df_result.empty
    assert len(df_result) == 1
    assert df_result.iloc[0]["date_id"] == 20101201
    assert df_result.iloc[0]["day_of_week"] == "Wednesday"

def test_load_sales(database_instance, loader_instance, sample_data):
    loader_instance.load_customers(sample_data)
    loader_instance.load_products(sample_data)
    loader_instance.load_dates(sample_data)

    loader_instance.load_sales(sample_data)

    df_result = database_instance.fetch_data("SELECT * FROM sales WHERE invoice_no IN ('536366', '536367', '536370');")

    assert not df_result.empty
    assert len(df_result) == 3
    assert set(df_result["invoice_no"]) == {"536366", "536367", "536370"}

def test_load(database_instance, loader_instance):
    loader_instance.load(sample_data_path)

    df_customers = database_instance.fetch_data(
        "SELECT * FROM customers WHERE customer_id IN ('17850', '13047', '12583');")
    assert len(df_customers) == 3

    df_products = database_instance.fetch_data(
        "SELECT * FROM products WHERE stock_code IN ('22633', '22632', '84879', '22728');")
    assert len(df_products) == 4

    df_dates = database_instance.fetch_data("SELECT * FROM dates WHERE date_id = 20101201;")
    assert len(df_dates) == 1

    df_sales = database_instance.fetch_data("SELECT * FROM sales WHERE invoice_no IN ('536366', '536367', '536370');")
    assert len(df_sales) == 3