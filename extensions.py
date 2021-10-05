import requests
import json
from config import API_KEY


class APIExceptions(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(values: list):
        if len(values) != 3:
            raise APIExceptions("Wrong number of parameters")
        quote, base, amount = values
        quote_ticker = quote
        base_ticker = base
        try:
            amount = float(amount)
        except ValueError:
            raise APIExceptions(f"Incorrect amount: {amount}")

        if quote == base:
            raise APIExceptions(f"Can't convert same currencies: {base}")

        request = requests.get(f"https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={API_KEY}")
        result = float(json.loads(request.content)["data"][f"{quote_ticker}{base_ticker}"]) * amount
        return round(result, 3)
