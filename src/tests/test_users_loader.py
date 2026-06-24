from unittest.mock import MagicMock

from loaders.users_loader import UsersLoader
from models.user import User


def test_load_silver():

    loader = UsersLoader()

    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    loader.connector.connect = MagicMock(
        return_value=mock_conn
    )

    users = [
        User(
            user_id=1,
            first_name="John",
            last_name="Doe"
        )
    ]

    loader.load_silver(users)

    assert mock_cursor.execute.called

    mock_conn.commit.assert_called_once()

    mock_cursor.close.assert_called_once()

    mock_conn.close.assert_called_once()