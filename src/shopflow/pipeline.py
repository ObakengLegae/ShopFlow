import logging

from extractor import Extractor
from transformer import Transformer
from loader import Loader
from database.database import Database

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

class Pipeline:

    def __init__(
            self,
            sql_file_path: str = None,
            raw_data_path: str = None,
            processed_data_path: str = None,
            database: Database = None,
            extractor: Extractor = None,
            transformer: Transformer = None,
            loader: Loader = None
    ):
        self.sql_file_path = sql_file_path or './sql/schema.sql'
        self.raw_data_path = raw_data_path or './data/raw/online_retail.csv'
        self.processed_data_path = processed_data_path or './data/processed/online_retail.csv'
        self.database = database or Database()
        self.extractor = extractor or Extractor()
        self.transformer = transformer or Transformer()
        self.loader = loader or Loader(database=self.database)

    def run(self):
        logger.info("Initializing pipeline...")

        try:
            logger.info("Preparing database...")
            self.database.create_tables(self.sql_file_path)

            logger.info(f"Extracting data from {self.raw_data_path}...")
            raw_data = self.extractor.extract_data(self.raw_data_path)
            if raw_data.empty:
                logger.warning("Extracted data is empty")
                return

            logger.info("Transforming raw data...")
            transformed_data = self.transformer.transform(raw_data)

            logger.info("Saving processed backup...")
            self.transformer.save_transformed_data(transformed_data)

            logger.info("Loading processed data into schema...")
            self.loader.load(transformed_data)

        except FileNotFoundError as e:
            logger.error(f"Missing required file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.run()