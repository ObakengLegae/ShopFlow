import pandas as pd
import os

class Extractor:
    def extract_data(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File {file_path} not found')

        df = pd.read_csv(file_path)
        return df
