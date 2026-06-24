class UsersQuality:

    def validate(self, bronze_rows):
        valid_rows = []
        invalid_rows = []

        for row in bronze_rows:
            user = row[0]

            if (user.get("id") is None) or (not user.get("firstName")) or (not user.get("lastName")):
                invalid_rows.append(row)
                continue

            valid_rows.append(row)

        return valid_rows, invalid_rows

    def validate_silver(self, silver_users):
        valid = [] 
        invalid = []

        for u in silver_users:
            if not u.user_id or not u.first_name:
                invalid.append(u)
            else:
                valid.append(u)

        return valid, invalid