from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

from connectors.postgres_connector import PostgresConnector
from migrations.init_db import init_db

from extractors.users_extractor import UsersExtractor
from transformers.users_transformer import UsersTransformer
from loaders.users_loader import UsersLoader
from quality.users_quality import UsersQuality
from utils.retry import retry


default_args = {
    "start_date": datetime(2024, 1, 1)
}


# =========================
# INIT DB
# =========================
def init_database_func():
    logger = logging.getLogger("init_db")

    try:
        logger.info("START init_db")

        conn = PostgresConnector().connect()
        init_db(conn)
        conn.close()

        logger.info("END init_db")

    except Exception as e:
        logger.error(f"init_db failed: {e}")
        raise


# =========================
# EXTRACT
# =========================
def extract_func(ti):
    logger = logging.getLogger("extract")

    try:
        logger.info("START extract")

        extractor = UsersExtractor()
        data = retry(extractor.extract, logger)

        logger.info(f"END extract | rows={len(data)}")

        return data

    except Exception as e:
        logger.error(f"extract failed: {e}")
        raise


# =========================
# BRONZE
# =========================
def bronze_func(ti, **context):
    logger = logging.getLogger("bronze")

    try:
        logger.info("START bronze")

        loader = UsersLoader()
        raw_users = ti.xcom_pull(task_ids="extract")

        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        logger.info(f"batch_id={batch_id} | rows={len(raw_users)}")

        retry(lambda: loader.load_bronze(raw_users, batch_id), logger)

        logger.info("END bronze")

        return batch_id

    except Exception as e:
        logger.error(f"bronze failed: {e}")
        raise


# =========================
# SILVER
# =========================
def silver_func(ti):
    logger = logging.getLogger("silver")

    try:
        logger.info("START silver")

        loader = UsersLoader()
        transformer = UsersTransformer()
        quality = UsersQuality()

        batch_id = ti.xcom_pull(task_ids="bronze")

        bronze_rows = loader.get_bronze_data(batch_id)
        users = transformer.transform(bronze_rows)

        valid_users, invalid_users = quality.validate_silver(users)

        logger.info(
            f"valid={len(valid_users)} | invalid={len(invalid_users)}"
        )

        if invalid_users:
            logger.warning(f"invalid rows detected={len(invalid_users)}")

        retry(lambda: loader.load_silver(valid_users), logger)

        logger.info("END silver")

    except Exception as e:
        logger.error(f"silver failed: {e}")
        raise


# =========================
# GOLD
# =========================
def gold_func():
    logger = logging.getLogger("gold")

    try:
        logger.info("START gold")

        loader = UsersLoader()
        retry(loader.load_gold, logger)

        logger.info("END gold")

    except Exception as e:
        logger.error(f"gold failed: {e}")
        raise


# =========================
# DAG
# =========================
with DAG(
    dag_id="users_pipeline",
    schedule=None,
    default_args=default_args,
    catchup=False
) as dag:

    t_init = PythonOperator(
        task_id="init_db",
        python_callable=init_database_func
    )

    t_extract = PythonOperator(
        task_id="extract",
        python_callable=extract_func
    )

    t_bronze = PythonOperator(
        task_id="bronze",
        python_callable=bronze_func
    )

    t_silver = PythonOperator(
        task_id="silver",
        python_callable=silver_func
    )

    t_gold = PythonOperator(
        task_id="gold",
        python_callable=gold_func
    )


t_init >> t_extract >> t_bronze >> t_silver >> t_gold