from src.shopflow.extractor import extract_data
from transformer import transform
from transformer import save_transformed_data

def main():
    raw_data_path = './data/raw/uci/Online Retail.csv'

    raw_data = extract_data(raw_data_path)

    transformed_data = transform(raw_data)

    save_transformed_data(transformed_data)

if __name__ == '__main__':
    main()