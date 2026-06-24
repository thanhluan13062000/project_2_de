import json
from config.settings import settings
from connectors.postgres_connector import PostgresConnector
from psycopg2.extras import (
    execute_values,
)  # ← THÊM IMPORT NÀY ĐỂ INSERT NHANH


class UsersLoader:

    def __init__(self):
        self.connector = PostgresConnector()

    def load_bronze(self, raw_users, batch_id):
        conn = self.connector.connect()
        cursor = conn.cursor()

        for user in raw_users:
            cursor.execute(
                f"""
                INSERT INTO {settings.db_schema}.bronze_users
                (batch_id,raw_data)
                VALUES (%s, %s)
                """,
                (batch_id, json.dumps(user)),
            )

        conn.commit()
        cursor.close()
        conn.close()

    def get_bronze_data(self, batch_id):
        conn = self.connector.connect()
        cursor = conn.cursor()
        cursor.execute(
            f"""SELECT raw_data FROM {settings.db_schema}.bronze_users WHERE batch_id = %s""",
            (batch_id,),
        )
        bronze_rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return bronze_rows

    # ==============================================================================
    # 🚀 THÊM HÀM NÀY ĐỂ LƯU DỮ LIỆU LỖI (INVALIDATED ROWS)
    # ==============================================================================
    def load_invalidated_rows(self, invalidated_rows, batch_id):
        if not invalidated_rows:
            return
        conn = self.connector.connect()
        cursor = conn.cursor()
        data_to_insert = [(json.dumps(row[0]), batch_id) for row in invalidated_rows]
        query = f"""
            INSERT INTO {settings.db_schema}.rejected_users (raw_data, batch_id)
            VALUES %s
        """
        try:
            execute_values(cursor, query, data_to_insert)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Lỗi khi lưu dữ liệu rác vào bảng rejected_users: {e}")
        finally:
            cursor.close()
            conn.close()

    def load_silver(self, users):
        conn = self.connector.connect()
        cursor = conn.cursor()

        for u in users:
            cursor.execute(
                f"""
                INSERT INTO {settings.db_schema}.silver_users
                (user_id, first_name, last_name)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO NOTHING
            """,
                (u.user_id, u.first_name, u.last_name),
            )

        conn.commit()
        cursor.close()
        conn.close()

    def load_gold(self):
        conn = self.connector.connect()
        cursor = conn.cursor()

        cursor.execute(f"""
            INSERT INTO {settings.db_schema}.gold_users (user_id, full_name)
            SELECT
                user_id,
                first_name || ' ' || last_name
            FROM {settings.db_schema}.silver_users
            ON CONFLICT (user_id) DO NOTHING
        """)

        conn.commit()
        cursor.close()
        conn.close()    