import pytest

from src.shopflow.pipeline import Pipeline
from src.shopflow.database.database import Database

sample_data_path = "./tests/resources/raw_csv_with_null_values.csv"
empty_data_path = "./tests/resources/empty_data.csv"
not_found_data_path = "./tests/resources/not_found.csv"

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

def test_pipeline_success(database_instance):

    pipeline = Pipeline(
        sql_file_path=database_instance.default_sql,
        raw_data_path=sample_data_path,
        database=database_instance
    )
    pipeline.run()

    df_customers = database_instance.fetch_data("SELECT * FROM customers;")
    assert len(df_customers) == 3

    df_products = database_instance.fetch_data("SELECT * FROM products;")
    assert len(df_products) == 8

    df_dates = database_instance.fetch_data("SELECT * FROM dates;")
    assert len(df_dates) == 2

    df_sales = database_instance.fetch_data("SELECT DISTINCT invoice_no FROM sales;")
    assert len(df_sales) == 3

def test_pipeline_with_empty_data(database_instance):

    pipeline = Pipeline(
        sql_file_path=database_instance.default_sql,
        raw_data_path=empty_data_path,
        database=database_instance
    )

    pipeline.run()

    df_sales = database_instance.fetch_data("SELECT * FROM sales;")
    assert len(df_sales) == 0


def def_test_pipeline_data_file_not_found(database_instance):

    pipeline = Pipeline(
        sql_file_path=database_instance.default_sql,
        raw_data_path=not_found_data_path,
        database=database_instance
    )

    with pytest.raises(FileNotFoundError):
        pipeline.run()