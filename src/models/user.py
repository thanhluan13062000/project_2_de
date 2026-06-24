class User:
    def __init__(
        self,
        user_id: int,
        first_name: str,
        last_name: str
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
    
    def __repr__(self):

        return (
            f"User("
            f"user_id={self.user_id}, "
            f"first_name='{self.first_name}', "
            f"last_name='{self.last_name}'"
            f")"
        )
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }