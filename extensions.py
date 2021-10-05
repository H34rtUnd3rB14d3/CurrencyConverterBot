import requests
import json
from config import API_KEY
from collections import defaultdict


class APIExceptions(Exception):
    pass

class UserInfo:
    def __init__(self):
        self.from_cur = "USD"
        self.to_cur = "RUB"

class UserDB:
    def __init__(self):
        self.db = defaultdict(UserInfo)

    def change_from(self, user_id, value):
        self.db[user_id].from_cur = value

    def change_to(self, user_id, value):
        self.db[user_id].to_cur = value

    def get_pair(self, user_id):
        return self.db[user_id].from_cur, self.db[user_id].to_cur



class Converter:
    @staticmethod
    def get_price(values: list):
        if len(values) != 3:
            raise APIExceptions("Wrong number of parameters")
        quote, base, amount = values
        quote_ticker = quote
        base_ticker = base
        print(quote_ticker, base_ticker)
        try:
            amount = float(amount)
        except ValueError:
            raise APIExceptions(f"Incorrect amount: {amount}")

        if quote == base:
            raise APIExceptions(f"Can't convert same currencies: {base}")

        request = requests.get(f"https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={API_KEY}")
        result = float(json.loads(request.content)["data"][f"{quote_ticker}{base_ticker}"]) * amount
        return round(result, 3)
