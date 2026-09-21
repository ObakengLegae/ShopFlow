from sqlalchemy import create_engine, text


def initialize_database():

    engine = create_engine('postgresql://postgres:password@localhost:5432/ecommerce_db')

    with open('sql/schema.sql', 'r') as file:
        sql_script = file.read()

    with engine.begin() as connection:
        connection.execute(text(sql_script))

    print("Database tables created successfully!")


if __name__ == "__main__":
    initialize_database()