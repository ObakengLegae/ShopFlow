import logging
import os
from datetime import datetime

from src.shopflow.extractor import Extractor
from src.shopflow.transformer import Transformer
from src.shopflow.loader import Loader
from src.shopflow.database.database import Database
from src.shopflow.uploader import Uploader

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
            loader: Loader = None,
            uploader: Uploader = None
    ):
        self.sql_file_path = sql_file_path or './sql/schema.sql'
        self.raw_data_path = raw_data_path or './data/raw/uci/online_retail.csv'

        if processed_data_path is None:
            base_name = os.path.basename(self.raw_data_path)
            name, extension = os.path.splitext(base_name)

            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

            self.processed_data_path = f'./data/processed/{name}_{timestamp}{extension}'
        else:
            self.processed_data_path = processed_data_path

        self.database = database or Database()
        self.extractor = extractor or Extractor()
        self.transformer = transformer or Transformer()
        self.loader = loader or Loader(database=self.database)
        self.uploader = uploader or Uploader()

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

            logger.info(f"Saving processed backup to {self.processed_data_path}...")
            os.makedirs(os.path.dirname(self.processed_data_path), exist_ok=True)
            self.transformer.save_transformed_data(transformed_data, file_path=self.processed_data_path)

            logger.info("Uploading processed data to s3...")
            self.uploader.upload(self.processed_data_path)

            logger.info("Loading processed data into schema...")
            self.loader.load(transformed_data)

        except FileNotFoundError as e:
            logger.error(f"Missing required file: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

if __name__ == '__main__':
    database = Database()
    uploader = Uploader(bucket_name=None)
    pipeline = Pipeline(
        sql_file_path='./sql/schema.sql',
        raw_data_path='data/raw/uci/online_retail.csv',
        database=database,
        uploader=uploader
    )
    pipeline.run()