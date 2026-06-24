import time

def retry(func, logger, retries=3, delay=2):
    """
    Hàm helper dùng chung cho toàn bộ dự án để tự động chạy lại tác vụ nếu lỗi.
    """
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            logger.warning(f"Thử lại lần {i+1}/{retries} thất bại do lỗi: {e}")
            if i < retries - 1:
                time.sleep(delay)
                
    raise Exception(f"Đã thử lại {retries} lần nhưng vẫn thất bại hoàn toàn.")