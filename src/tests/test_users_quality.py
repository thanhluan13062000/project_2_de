from quality.users_quality import UsersQuality


# --- KỊCH BẢN 1: HÀNG NGON CHẠY CHUẨN ---
def test_valid_user():
    quality = UsersQuality()
    rows = [({"id": 1, "firstName": "John", "lastName": "Doe"},)]
    valid_rows, _ = quality.validate(rows)
    assert len(valid_rows) == 1


# --- KỊCH BẢN 2: THỬ NGHIỆM LỖI ID ---
def test_missing_id():
    quality = UsersQuality()
    rows = [({"id": None, "firstName": "John", "lastName": "Doe"},)]
    valid_rows, invalid_rows = quality.validate(rows)
    assert len(valid_rows) == 0
    assert len(invalid_rows) == 1


# --- KỊCH BẢN 3: THỬ NGHIỆM LỖI FIRSTNAME (MỚI THÊM) ---
def test_missing_first_name():
    quality = UsersQuality()
    rows = [
        (
            {
                "id": 1,
                "firstName": None,  # ← Giả lập tình huống firstName bị rỗng/None
                "lastName": "Doe",
            },
        )
    ]
    valid_rows, invalid_rows = quality.validate(rows)

    # Khẳng định: Thằng này mất tên thì rổ sạch phải bằng 0, rổ lỗi phải bằng 1
    assert len(valid_rows) == 0
    assert len(invalid_rows) == 1


# --- KỊCH BẢN 4: THỬ NGHIỆM LỖI LASTNAME (MỚI THÊM) ---
def test_missing_last_name():
    quality = UsersQuality()
    rows = [
        (
            {
                "id": 1,
                "firstName": "John",
                "lastName": "",  # ← Giả lập tình huống lastName bị chuỗi rỗng ""
            },
        )
    ]
    valid_rows, invalid_rows = quality.validate(rows)

    # Khẳng định: Thằng này mất họ thì rổ sạch cũng phải bằng 0, rổ lỗi phải bằng 1
    assert len(valid_rows) == 0
    assert len(invalid_rows) == 1