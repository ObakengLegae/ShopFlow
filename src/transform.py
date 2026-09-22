import pandas as pd
import os

def transform(df):

    df = df.rename(columns={
        'InvoiceNo': 'invoice_no',
        'StockCode': 'stock_code',
        'Description': 'description',
        'Quantity': 'quantity',
        'InvoiceDate': 'invoice_date',
        'UnitPrice': 'unit_price',
        'CustomerID': 'customer_id',
        'Country': 'country'
    })

    df['description'] = df['description'].fillna("unknown").astype(str)
    df['customer_id'] = df['customer_id'].fillna("unknown").astype(str)
    df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%m/%d/%y %H:%M')

    df['date_id'] = df['invoice_date'].dt.strftime('%Y%m%d').astype(int)
    df['full_date'] = df['invoice_date'].dt.date
    df['year'] = df['invoice_date'].dt.year
    df['month'] = df['invoice_date'].dt.month
    df['day'] = df['invoice_date'].dt.day
    df['quarter'] = df['invoice_date'].dt.quarter
    df['day_of_week'] = df['invoice_date'].dt.day_name()

    df['total_amount'] = df['quantity'] * df['unit_price']

    return df

def save_transformed_data(df):

    path = './data/processed/uci/'
    os.makedirs(path, exist_ok=True)

    df.to_csv(path + 'processed_data.csv', index=False)

    expected_result = './data/processed/uci/processed_data.csv'

    if os.path.exists(expected_result):
        print(f"Data saved to csv at {expected_result}")