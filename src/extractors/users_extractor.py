from connectors.http_client import HttpClient
from config.settings import settings


class UsersExtractor:

    def __init__(self):
        self.client = HttpClient()

    def extract(self):
        response = self.client.get(settings.users_url)
        return response["users"]