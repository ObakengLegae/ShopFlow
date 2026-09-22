from src.shopflow.extractor import Extractor


def test_extract():
    extractor = Extractor()
    test_csv = "./tests/resources/test_csv_one.csv"
    data = extractor.extract_data(test_csv)

    expected_columns = ["InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate", "UnitPrice", "CustomerID", "Country"]

    for col in data:
        assert col in expected_columns