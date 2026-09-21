import pandas as pd
import os

def extract_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File {file_path} not found')

    df = pd.read_csv(file_path)
    return df

if __name__ == '__main__':
    csv_path = "./data/raw/uci/Online Retail.csv"
    csv_df = extract_data(csv_path)