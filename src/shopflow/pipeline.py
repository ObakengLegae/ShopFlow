from extractor import Extractor
from transformer import Transformer
from loader import Loader
from database.database import Database

"""
self.sql_file_path = './sql/schema.sql'
        self.raw_data_path = './data/raw/uci/Online Retail.csv'
        self.processed_data_path = './data/processed/uci/processed_data.csv'
        self.database = Database()
        self.extractor = Extractor()
        self.transformer = Transformer()
        self.loader = Loader(database=self.database)
"""
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
        self.database.create_tables(self.sql_file_path)

        raw_data = self.extractor.extract_data(self.raw_data_path)

        transformed_data = self.transformer.transform(raw_data)

        self.transformer.save_transformed_data(transformed_data)

        self.loader.load(transformed_data)


if __name__ == '__main__':
    pipeline = Pipeline()
    pipeline.run()