import pandas as pd

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

    df['description'] = df['description'].fillna("Unknown description").astype(str)
    df['customer_id'] = df['customer_id'].fillna("Unknown customer_id").astype(str)
    df['invoice_no'] = pd.to_datetime(df['invoice_no'], format='%m/%d/%y %H:%M')

    #transform into processed csv in data, include other schema details