from models.user import User


class UsersTransformer:

    def transform(self, bronze_rows):
        users = []

        for row in bronze_rows:
            item = row[0] 
            
            users.append(
                User(
                    user_id=item["id"],
                    first_name=item["firstName"],
                    last_name=item["lastName"]
                )
            )
        return users