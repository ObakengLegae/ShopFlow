from src.shopflow.extract import extract_data

def test_extract():
    test_csv = "./tests/resources/test_csv_one.csv"
    data = extract_data(test_csv)

    expected_columns = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]

    for col in data:
        assert col in expected_columns