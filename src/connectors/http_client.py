import requests

class HttpClient:
    def get(self,url: str):
        response = requests.get(url)
        response.raise_for_status()
        return response.json()