import pandas as pd
import os
import logging


logger = logging.getLogger(__name__)

class Extractor:
    def extract_data(self, file_path: str):
        """Extract data from csv file, return a Pandas dataframe."""

        if not os.path.exists(file_path):
            logger.error(f"Failed extraction: File {file_path} not found")
            raise FileNotFoundError(f'File {file_path} not found')

        logger.info(f"Extracting data from {file_path}...")

        try:
            df = pd.read_csv(file_path)
            logger.info(f"Successfully extracted data from {file_path}")

            return df
        except pd.errors.ParserError as e:
            logger.error(f"Pandas failed to parse the CSV file {file_path}: {e}")
            raise
        except UnicodeDecodeError as e:
            logger.error(f"Encoding issue with {file_path}: {e}")
            raise
