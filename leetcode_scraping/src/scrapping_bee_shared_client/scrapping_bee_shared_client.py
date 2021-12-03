import json

from scrapingbee import ScrapingBeeClient
from requests import Response


class ScrBeeSharedClient:
    API_KEY_LIMIT_REACHED_CONTENT = \
        b'{"message": "Monthly API calls limit reached: 1000"}\n'

    def __init__(self, api_keys_json_path):
        self.api_keys_json_path_ = api_keys_json_path
        self.current_api_key = None
        self.current_client = None
        self.__update_client()

    def get(self, *args, **kwargs) -> Response:
        response = self.current_client.get(*args, **kwargs)
        if response.content == self.API_KEY_LIMIT_REACHED_CONTENT:
            with open(self.api_keys_json_path_, 'r+') as api_keys_json:
                keys_dict = json.load(api_keys_json)
                keys_dict[self.current_api_key] = 0
                api_keys_json.seek(0)
                json.dump(keys_dict, api_keys_json)
                api_keys_json.truncate()
            self.__update_client()
            return self.current_client.get(*args, **kwargs)
        return response

    def __get_next_valid_api_key(self) -> str:
        with open(self.api_keys_json_path_, 'r') as api_keys_json:
            keys_dict = json.load(api_keys_json)
            for api_key, status in keys_dict.items():
                if status:
                    return api_key
            raise RuntimeError(f'No available api keys left.')

    def __update_client(self):
        self.current_api_key = self.__get_next_valid_api_key()
        self.current_client = ScrapingBeeClient(self.current_api_key)
