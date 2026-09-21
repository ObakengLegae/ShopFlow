CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Customers Table
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    country_id INT REFERENCES countries(country_id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Products Catalog Table
CREATE TABLE products (
    stock_code VARCHAR(30) PRIMARY KEY,
    description VARCHAR(255),
    latest_unit_price NUMERIC(10, 2) DEFAULT 0.00,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Invoices / Orders Header
CREATE TABLE invoices (
    invoice_no VARCHAR(20) PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id) ON DELETE SET NULL,
    country_id INT NOT NULL REFERENCES countries(country_id),
    invoice_date TIMESTAMP NOT NULL,
    is_cancellation BOOLEAN GENERATED ALWAYS AS (invoice_no LIKE 'C%') STORED
);

-- 5. Invoice Line Items
CREATE TABLE invoice_items (
    invoice_item_id BIGSERIAL PRIMARY KEY,
    invoice_no VARCHAR(20) NOT NULL REFERENCES invoices(invoice_no) ON DELETE CASCADE,
    stock_code VARCHAR(30) NOT NULL REFERENCES products(stock_code),
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    line_total NUMERIC(12, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED
);