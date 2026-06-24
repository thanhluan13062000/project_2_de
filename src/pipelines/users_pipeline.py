from extractors.users_extractor import UsersExtractor
from transformers.users_transformer import UsersTransformer
from loaders.users_loader import UsersLoader
from quality.users_quality import UsersQuality
from datetime import datetime
from utils.retry import retry 


class UsersPipeline:

    def __init__(self, logger):
        self.extractor = UsersExtractor()
        self.transformer = UsersTransformer()
        self.loader = UsersLoader()
        self.quality = UsersQuality()
        self.logger = logger

    def run(self):
        batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        self.logger.info(
            f"Starting pipeline - batch_id={batch_id}"
        )

        # --- EXTRACT ---
        try:
            # Truyền thêm self.logger vào làm tham số thứ 2
            raw_users = retry(self.extractor.extract, self.logger)
            self.logger.info(f"Extracted {len(raw_users)} users")
        except Exception as e:
            self.logger.error(f"Extract failed after retries: {e}")
            return
    
        # --- BRONZE ---
        try:
            # Dùng lambda và truyền self.logger vào
            retry(lambda: self.loader.load_bronze(raw_users,batch_id), self.logger)
            self.logger.info("Loaded bronze")
        except Exception as e:
            self.logger.error(f"Bronze load failed after retries: {e}")
            return

        # --- TRANSFORM (Giữ nguyên không retry) ---
        try:
            bronze_rows = self.loader.get_bronze_data(batch_id)
            validated_rows,invalidated_rows = self.quality.validate(bronze_rows)
            silver_users = self.transformer.transform(validated_rows)
            self.logger.info(f"Transformed to {len(silver_users)} silver users")
            if len(invalidated_rows) > 0:
                self.loader.load_invalidated_rows(invalidated_rows, batch_id)
        except Exception as e:
            self.logger.error(f"Transform failed: {e}")
            return

        # --- SILVER ---
        try:
            retry(lambda: self.loader.load_silver(silver_users), self.logger)
            self.logger.info("Loaded silver layer")
        except Exception as e:
            self.logger.error(f"Silver load failed after retries: {e}")
            return

        # --- GOLD ---
        try:
            retry(self.loader.load_gold, self.logger)
            self.logger.info("Loaded gold layer")
        except Exception as e:
            self.logger.error(f"Gold load failed after retries: {e}")
            return

        self.logger.info("PIPELINE DONE SUCCESSFULLY")