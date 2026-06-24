from unittest.mock import MagicMock
from loaders.users_loader import UsersLoader
from pipelines.users_pipeline import UsersPipeline


# --- TEST CASE 1: KIỂM TRA TOÀN BỘ PIPELINE ---
def test_pipeline_run():
    logger = MagicMock()
    pipeline = UsersPipeline(logger)

    pipeline.extractor.extract = MagicMock(
        return_value=[{"id": 1, "firstName": "John", "lastName": "Doe"}]
    )

    pipeline.loader.load_bronze = MagicMock()
    pipeline.loader.get_bronze_data = MagicMock(
        return_value=[({"id": 1, "firstName": "John", "lastName": "Doe"},)]
    )

    pipeline.loader.load_silver = MagicMock()
    pipeline.loader.load_gold = MagicMock()

    pipeline.run()

    pipeline.loader.load_bronze.assert_called_once()
    pipeline.loader.load_silver.assert_called_once()
    pipeline.loader.load_gold.assert_called_once()


# --- TEST CASE 2: KIỂM TRA HÀM GHI VÀO BRONZE (ĐÃ SỬA THỤT DÒNG) ---
def test_load_bronze():
    loader = UsersLoader()

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Giả lập: Khi gọi conn.cursor() thì trả về đối tượng cursor đóng thế
    mock_conn.cursor.return_value = mock_cursor
from unittest.mock import MagicMock

from loaders.users_loader import UsersLoader
from pipelines.users_pipeline import UsersPipeline


# --- TEST CASE 1: KIỂM TRA TOÀN BỘ PIPELINE ---
def test_pipeline_run():
    logger = MagicMock()
    pipeline = UsersPipeline(logger)

    pipeline.extractor.extract = MagicMock(
        return_value=[{"id": 1, "firstName": "John", "lastName": "Doe"}]
    )

    pipeline.loader.load_bronze = MagicMock()
    pipeline.loader.get_bronze_data = MagicMock(
        return_value=[({"id": 1, "firstName": "John", "lastName": "Doe"},)]
    )

    pipeline.loader.load_silver = MagicMock()
    pipeline.loader.load_gold = MagicMock()

    pipeline.run()

    pipeline.loader.load_bronze.assert_called_once()
    pipeline.loader.load_silver.assert_called_once()
    pipeline.loader.load_gold.assert_called_once()


# --- TEST CASE 2: KIỂM TRA HÀM GHI VÀO BRONZE (ĐÃ SỬA THỤT DÒNG) ---
def test_load_bronze():
    loader = UsersLoader()

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Giả lập: Khi gọi conn.cursor() thì trả về đối tượng cursor đóng thế
    mock_conn.cursor.return_value = mock_cursor

    # Giả lập: Khi gọi connector.connect() thì trả về đối tượng conn đóng thế
    loader.connector.connect = MagicMock(return_value=mock_conn)

    raw_users = [{"id": 1, "firstName": "John", "lastName": "Doe"}]

    # Chạy thử hàm với batch_id giả lập thời gian năm 2026
    loader.load_bronze(raw_users, "20260624_100000")

    # KIỂM TRA: Hàm execute phải được gọi đúng 1 lần (vì chỉ có 1 user đầu vào)
    mock_cursor.execute.assert_called_once()

    # KIỂM TRA: Đã gọi lệnh commit để lưu dữ liệu chưa
    mock_conn.commit.assert_called_once()

    # KIỂM TRA: Đã đóng cursor và connection để tránh rò rỉ bộ nhớ chưa
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# --- TEST CASE 3: KIỂM TRA HÀM ĐỌC TỪ BRONZE (ĐÃ SỬA THỤT DÒNG) ---
def test_get_bronze_data():
    loader = UsersLoader()

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    # Giả lập dữ liệu trả về từ Postgres khi gọi fetchall()
    mock_cursor.fetchall.return_value = [({"id": 1},)]

    loader.connector.connect = MagicMock(return_value=mock_conn)

    result = loader.get_bronze_data("20260624_100000")

    # KIỂM TRA: Kết quả trả về phải có độ dài bằng 1
    assert len(result) == 1

    # KIỂM TRA: Đảm bảo dọn dẹp đóng kết nối sau khi đọc xong
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()
    loader.connector.connect = MagicMock(return_value=mock_conn)

    raw_users = [{"id": 1, "firstName": "John", "lastName": "Doe"}]

    # Chạy thử hàm với batch_id giả lập thời gian năm 2026
    loader.load_bronze(raw_users, "20260624_100000")

    # KIỂM TRA: Hàm execute phải được gọi đúng 1 lần (vì chỉ có 1 user đầu vào)
    mock_cursor.execute.assert_called_once()

    # KIỂM TRA: Đã gọi lệnh commit để lưu dữ liệu chưa
    mock_conn.commit.assert_called_once()

    # KIỂM TRA: Đã đóng cursor và connection để tránh rò rỉ bộ nhớ chưa
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


# --- TEST CASE 3: KIỂM TRA HÀM ĐỌC TỪ BRONZE (ĐÃ SỬA THỤT DÒNG) ---
def test_get_bronze_data():
    loader = UsersLoader()

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    # Giả lập dữ liệu trả về từ Postgres khi gọi fetchall()
    mock_cursor.fetchall.return_value = [({"id": 1},)]

    loader.connector.connect = MagicMock(return_value=mock_conn)

    result = loader.get_bronze_data("20260624_100000")

    # KIỂM TRA: Kết quả trả về phải có độ dài bằng 1
    assert len(result) == 1

    # KIỂM TRA: Đảm bảo dọn dẹp đóng kết nối sau khi đọc xong
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()    