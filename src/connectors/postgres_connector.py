import psycopg2
from config.settings import settings

class PostgresConnector:
    def connect(self):
        connection = psycopg2.connect(
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password
        )

        return connection