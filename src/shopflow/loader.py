import pandas as pd
from src.shopflow.database.database import Database
from src.shopflow.extractor import Extractor

class Loader:
    def __init__(self, database: Database):
        self.database = database

    def load(self, processed_data: pd.DataFrame):
        """Adds all data to database"""
        print("Adding data to database")
        self.load_customers(processed_data)
        self.load_products(processed_data)
        self.load_dates(processed_data)
        self.load_sales(processed_data)


    def load_customers(self, data: pd.DataFrame):
        """Adds customer data to database"""
        customers = data[
            ["customer_id", "country"]
        ].drop_duplicates(subset="customer_id")

        self.database.insert_data(customers, "customers")
        print("Customers added to database")

    def load_products(self, data: pd.DataFrame):
        """Adds product data to database"""
        products = data[
            ["stock_code", "description"]
        ].drop_duplicates(subset="stock_code")

        self.database.insert_data(products, "products")
        print("Products added to database")

    def load_dates(self, data: pd.DataFrame):
        """Adds dates to database"""
        dates = data[
            ["date_id", "full_date", "year", "month", "day", "quarter", "day_of_week"]
        ].drop_duplicates(subset="date_id")

        self.database.insert_data(dates, "dates")
        print("Dates added to database")

    def load_sales(self, data: pd.DataFrame):
        """Adds sales data to database"""
        sales = data[
            ["invoice_no", "customer_id", "stock_code", "date_id", "quantity", "unit_price", "total_amount",
             "sale_timestamp"]
        ].drop_duplicates(subset="invoice_no")

        self.database.insert_data(sales, "sales")
        print("Sales added to database")