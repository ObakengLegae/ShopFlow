CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    country VARCHAR(50)
);

CREATE TABLE products (
    stock_code VARCHAR(20) PRIMARY KEY,
    description VARCHAR(255)
);

CREATE TABLE dates (
    date_id INT PRIMARY KEY, -- FORMAT: YYYYMMDD
    full_date DATE,
    year INT,
    month INT,
    day INT,
    quarter INT,
    day_of_week VARCHAR(10)
);

CREATE TABLE sales (
    sale_id SERIAL PRIMARY KEY,
    invoice_no VARCHAR(20),
    customer_id VARCHAR(10) REFERENCES customers(customer_id),
    stock_code VARCHAR(20) REFERENCES products(stock_code),
    date_id INT REFERENCES dates(date_id),
    quantity INT,
    unit_price NUMERIC(10, 2),
    total_amount NUMERIC(10, 2),
    sale_timestamp TIMESTAMP
);