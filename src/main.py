from pipelines.users_pipeline import UsersPipeline
from utils.logger import get_logger
from migrations.init_db import init_db
from connectors.postgres_connector import PostgresConnector


if __name__ == "__main__":

    logger = get_logger("users_pipeline")

    conn = PostgresConnector().connect()
    init_db(conn)

    pipeline = UsersPipeline(logger)
    pipeline.run()