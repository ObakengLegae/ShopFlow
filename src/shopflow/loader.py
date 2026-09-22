import pandas as pd
from numpy.core import records
from psycopg2.extras import execute_values
from sqlalchemy.engine import row

from src.shopflow.database import database
from src.shopflow.database.database import Database
from src.shopflow.extract import extract_data

class Loader:
    def __init__(self, database: Database):
        self.database = database

    def load(self, file_path: str):
        processed_data = extract_data(file_path)

        self.load_customers(processed_data)


    def load_customers(self, data: pd.DataFrame):
        customers = data[
            ["customer_id", "country"]
        ].drop_duplicates(subset="customer_id")

        self.database.insert_data(customers, "customer_id")

    def load_products(self, data: pd.DataFrame):
        products = data[
            ["stock_code", "description"]
        ].drop_duplicates(subset="stock_code")

        self.database.insert_data(products, "stock_code")
