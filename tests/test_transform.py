import pytest
import pandas as pd

from src.shopflow.extractor import Extractor
from src.shopflow.transformer import Transformer

@pytest.fixture
def sample_transformed_data():
    extractor = Extractor()
    transformer = Transformer()
    test_csv = "./tests/resources/raw_csv_with_null_values.csv"
    data = extractor.extract_data(test_csv)
    transformed_data = transformer.transform(data)
    return transformed_data


def test_columns_are_added(sample_transformed_data):
    expected_columns = [
        "invoice_no",
        "stock_code",
        "description",
        "quantity",
        "sale_timestamp",
        "unit_price",
        "customer_id",
        "country",
        "date_id",
        "full_date",
        "year",
        "month",
        "day",
        "quarter",
        "day_of_week",
        "total_amount"
    ]

    for col in sample_transformed_data:
        assert col in expected_columns


def test_invoice_date_is_datetime(sample_transformed_data):
    assert pd.api.types.is_datetime64_any_dtype(sample_transformed_data['sale_timestamp']), \
        "invoice_date column was not converted to a datetime object."


def test_null_customer_ids_are_unknown(sample_transformed_data):
    missing_customer_rows = sample_transformed_data[sample_transformed_data['invoice_no'] == 536876]

    for customer_id in missing_customer_rows['customer_id']:
        assert customer_id == 'unknown', f"Expected 'unknown', but found {customer_id}"

    assert sample_transformed_data['customer_id'].isnull().sum() == 0, \
        "Found null values remaining in the customer_id column."


def test_new_columns_have_values(sample_transformed_data):
    new_columns = ['date_id', 'full_date', 'year', 'month', 'day', 'quarter', 'day_of_week', 'total_amount']

    for col in new_columns:
        assert col in sample_transformed_data.columns, f"Column '{col}' is missing."

        assert sample_transformed_data[col].isnull().sum() == 0, f"Column '{col}' contains null values."

        if sample_transformed_data[col].dtype == object:
            assert (sample_transformed_data[col] == '').sum() == 0, f"Column '{col}' contains empty strings."