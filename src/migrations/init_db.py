from config.settings import settings


def init_db(conn):
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE SCHEMA IF NOT EXISTS {settings.db_schema};
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.db_schema}.bronze_users (
            id SERIAL PRIMARY KEY,
            batch_id VARCHAR(50),
            raw_data JSONB,
            ingested_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.db_schema}.silver_users (
            user_id INT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT
        );
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.db_schema}.gold_users (
            user_id INT PRIMARY KEY,
            full_name TEXT
        );
    """)
    conn.commit()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {settings.db_schema}.rejected_users (
            id SERIAL,
            raw_data JSONB,
            rejected_at TIMESTAMP DEFAULT NOW(),
            batch_id INT
        );
    """)