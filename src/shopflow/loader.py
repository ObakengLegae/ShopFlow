import logging

import pandas as pd
from src.shopflow.database.database import Database
from src.shopflow.extractor import Extractor

logger = logging.getLogger(__name__)

class Loader:
    """Isolates relation data tables and loads them into database"""
    def __init__(self, database: Database):
        self.database = database

    def load(self, processed_data: pd.DataFrame):
        """Loads all the data into the database in the correct relational order."""
        if processed_data is None or processed_data.empty:
            logger.warning("Empty DataFrame. Skipping load operations")
            return

        logger.info("Loading data")
        try:
            self.load_customers(processed_data)
            self.load_products(processed_data)
            self.load_dates(processed_data)
            self.load_sales(processed_data)
            logger.info("All tables successfully loaded")
        except KeyError as e:
            logger.error(f"Failed to find column during loading: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

    def load_customers(self, data: pd.DataFrame):
        """Isolates customer data and adds it to database"""
        logger.info("Isolating customer data")
        customers = data[
            ["customer_id", "country"]
        ].drop_duplicates(subset="customer_id")

        self.database.insert_data(customers, "customers")
        logger.info("Customers sent to database")

    def load_products(self, data: pd.DataFrame):
        """Isolates product data and adds it to database"""
        logger.info("Isolating product data")
        products = data[
            ["stock_code", "description"]
        ].drop_duplicates(subset="stock_code")

        self.database.insert_data(products, "products")
        logger.info("Products sent to database")

    def load_dates(self, data: pd.DataFrame):
        """Isolates date data and adds it to database"""
        logger.info("Isolating date data")
        dates = data[
            ["date_id", "full_date", "year", "month", "day", "quarter", "day_of_week"]
        ].drop_duplicates(subset="date_id")

        self.database.insert_data(dates, "dates")
        logger.info("Dates sent to database")

    def load_sales(self, data: pd.DataFrame):
        """Isolates sales data and adds it to database"""
        logger.info("Isolating sale data")
        sales = data[
            ["invoice_no", "customer_id", "stock_code", "date_id", "quantity", "unit_price", "total_amount",
             "sale_timestamp"]
        ].drop_duplicates(subset="invoice_no")

        self.database.insert_data(sales, "sales")
        logger.info("Sales sent to database")