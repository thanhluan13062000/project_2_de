import logging
import os

def get_logger(name: str):

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        # tạo folder logs nếu chưa có
        os.makedirs("logs", exist_ok=True)

        # log ra file
        file_handler = logging.FileHandler(f"logs/{name}.log")
        file_handler.setLevel(logging.INFO)

        # format log
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        # vẫn log ra terminal
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger