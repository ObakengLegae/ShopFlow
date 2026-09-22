from src.shopflow.extractor import Extractor
from transformer import Transformer

def main():
    extractor = Extractor()
    transformer = Transformer()

    raw_data_path = './data/raw/uci/Online Retail.csv'

    raw_data = extractor.extract_data(raw_data_path)

    transformed_data = transformer.transform(raw_data)

    transformer.save_transformed_data(transformed_data)

if __name__ == '__main__':
    main()