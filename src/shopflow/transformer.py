import pandas as pd
import os

def transform(df):

    df = df.rename(columns={
        'InvoiceNo': 'invoice_no',
        'StockCode': 'stock_code',
        'Description': 'description',
        'Quantity': 'quantity',
        'InvoiceDate': 'sale_timestamp',
        'UnitPrice': 'unit_price',
        'CustomerID': 'customer_id',
        'Country': 'country'
    })

    df['description'] = df['description'].fillna("unknown").astype(str)
    df['customer_id'] = df['customer_id'].fillna("unknown").astype(str)
    df['sale_timestamp'] = pd.to_datetime(df['sale_timestamp'], format='%m/%d/%y %H:%M')

    df['date_id'] = df['sale_timestamp'].dt.strftime('%Y%m%d').astype(int)
    df['full_date'] = df['sale_timestamp'].dt.date
    df['year'] = df['sale_timestamp'].dt.year
    df['month'] = df['sale_timestamp'].dt.month
    df['day'] = df['sale_timestamp'].dt.day
    df['quarter'] = df['sale_timestamp'].dt.quarter
    df['day_of_week'] = df['sale_timestamp'].dt.day_name()

    df['total_amount'] = df['quantity'] * df['unit_price']
    df['total_amount'] = df['total_amount'].map('{:.2f}'.format)

    return df

def save_transformed_data(df):

    path = './data/processed/uci/'
    os.makedirs(path, exist_ok=True)

    df.to_csv(path + 'test_processed_data.csv', index=False)

    expected_result = './data/processed/uci/test_processed_data.csv'

    if os.path.exists(expected_result):
        print(f"Data saved to csv at {expected_result}")