from transformers.users_transformer import UsersTransformer


def test_transform_single_user():

    transformer = UsersTransformer()

    bronze_rows = [
        (
            {
                "id": 1,
                "firstName": "John",
                "lastName": "Doe"
            },
        )
    ]

    users = transformer.transform(bronze_rows)

    assert len(users) == 1

    assert users[0].user_id == 1
    assert users[0].first_name == "John"
    assert users[0].last_name == "Doe"