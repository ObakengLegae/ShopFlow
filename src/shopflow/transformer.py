import pandas as pd
import os
import logging

logger = logging.getLogger(__name__)

class Transformer:
    def transform(self, df: pd.DataFrame):
        """Cleans and processes raw data"""
        if df is None or df.empty:
            logger.warning(f"Empty dataframe passed to transform, returning empty dataframe")
            return pd.DataFrame()

        logger.info('Transforming data')

        try:
            logger.debug("Renaming columns")
            df = df.rename(columns={
                'InvoiceNo': 'invoice_no',
                'StockCode': 'stock_code',
                'Description': 'description',
                'Quantity': 'quantity',
                'InvoiceDate': 'sale_timestamp',
                'UnitPrice': 'unit_price',
                'CustomerID': 'customer_id',
                'Country': 'country'
            })

            logger.debug("Adding placeholders to null values")
            df['description'] = df['description'].fillna("unknown").astype(str)
            df['customer_id'] = df['customer_id'].fillna("unknown").astype(str)

            logger.debug("Converting timestamps")
            df['sale_timestamp'] = pd.to_datetime(df['sale_timestamp'], format='%m/%d/%y %H:%M')

            logger.debug("Creating new date columns")
            df['date_id'] = df['sale_timestamp'].dt.strftime('%Y%m%d').astype(int)
            df['full_date'] = df['sale_timestamp'].dt.date
            df['year'] = df['sale_timestamp'].dt.year
            df['month'] = df['sale_timestamp'].dt.month
            df['day'] = df['sale_timestamp'].dt.day
            df['quarter'] = df['sale_timestamp'].dt.quarter
            df['day_of_week'] = df['sale_timestamp'].dt.day_name()

            logger.debug("Calculating total amount")
            df['total_amount'] = df['quantity'] * df['unit_price']
            df['total_amount'] = df['total_amount'].map('{:.2f}'.format)

            logger.info("Transformation complete")
            return df

        except KeyError as e:
            logger.error(f"Missing expected column: {e}")
            raise
        except ValueError as e:
            logger.error(f"Value error during transformation: {e}")
            raise
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise

#Todo: Implement logic to save the data using different file names
    def save_transformed_data(self, df: pd.DataFrame, file_path: str = './data/processed/uci/processed_data.csv'):
        """Saves transformed data to csv file"""
        if df is None or df.empty:
            logger.warning(f"Empty dataframe. Skipping save operation")
            return

        logger.info('Saving transformed backup')

        try:
            os.makedirs(file_path, exist_ok=True)

            df.to_csv(file_path + 'processed_data.csv', index=False)

            if os.path.exists(file_path):
                logger.info(f"Data saved to csv at: {file_path}")
            else:
                logger.error(f"Failed to verify saved file at {file_path}")

        except PermissionError as e:
            logger.error(f"Permission denied when saving data: {e}")
            raise
        except OSError as e:
            logger.error(f"OS error occurred when saving data: {e}")
            raise
        except ValueError as e:
            logger.error(f"An error occurred: {e}")
            raise