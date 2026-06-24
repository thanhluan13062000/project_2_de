from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    def __init__(self):

        # API
        self.base_url = os.getenv("BASE_URL")
        self.users_url = os.getenv("USERS_URL")
        self.products_url = os.getenv("PRODUCTS_URL")
        self.carts_url = os.getenv("CARTS_URL")

        # DATABASE
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")

        # SCHEMA
        self.db_schema = os.getenv("DB_SCHEMA")

        # ENV
        self.environment = os.getenv("ENVIRONMENT")

        self._validate()

    def _validate(self):

        required_vars = [
            "base_url",
            "users_url",
            "products_url",
            "carts_url",
            "db_host",
            "db_port",
            "db_name",
            "db_user",
            "db_password",
            "db_schema"
        ]

        for var in required_vars:
            if getattr(self, var) is None:
                raise ValueError(f"{var} is not set")

settings = Settings()