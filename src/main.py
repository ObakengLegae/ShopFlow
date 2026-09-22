import pandas as pd

from extract import extract_data
from transform import transform
from transform import save_transformed_data

def main():
    raw_data_path = './data/raw/uci/Online Retail.csv'

    raw_data = extract_data(raw_data_path)

    transformed_data = transform(raw_data)

    save_transformed_data(transformed_data)

if __name__ == '__main__':
    main()