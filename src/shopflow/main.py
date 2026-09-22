from extractor import Extractor
from transformer import Transformer
from loader import Loader
from database.database import Database

def main():
    database = Database()
    extractor = Extractor()
    transformer = Transformer()
    loader = Loader(database)

    sql_file_path = './sql/schema.sql'
    raw_data_path = './data/raw/uci/Online Retail.csv'

    database.create_tables(sql_file_path)

    raw_data = extractor.extract_data(raw_data_path)

    transformed_data = transformer.transform(raw_data)

    transformer.save_transformed_data(transformed_data)

    processed_data_path = './data/processed/uci/processed_data.csv'

    loader.load(processed_data_path)

if __name__ == '__main__':
    main()