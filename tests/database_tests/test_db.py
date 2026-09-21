import pytest
from sqlalchemy import create_engine, text
from src.database.init_db import initialize_database

@pytest.fixture
def db_engine():
    engine = create_engine('postgresql://postgres:password@localhost:5432/ecommerce_db')
    return engine

def test_tables_created_successfully(db_engine):
    initialize_database(db_engine)
    check_tables_query = text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)

    with db_engine.connect() as connection:
        result = connection.execute(check_tables_query)
        created_tables = [row[0] for row in result]

    expected_tables = ['countries','customers', 'products', 'invoices', 'invoice_items']

    for table in expected_tables:
        assert table in created_tables, f"Table '{table}' was not created!"