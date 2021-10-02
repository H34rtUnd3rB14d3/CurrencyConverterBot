import requests
from config import exchanger, API_KEY


class APIExceptions(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(values: list):
        if len(values) != 3:
            raise APIExceptions("Wrong number of parameters")
        quote, base, amount = values

        try:
            quote_ticker = exchanger[quote]
        except KeyError:
            raise APIExceptions(f"This bot doesn't support currency: {base}")

        try:
            base_ticker = exchanger[base]
        except KeyError:
            raise APIExceptions(f"This bot doesn't support currency: {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIExceptions(f"Incorrect amount: {amount}")

        if quote == base:
            raise APIExceptions(f"Can't convert same currencies: {base}")

        request = requests.get(f"https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key={API_KEY}")
        result = float(request.json()["data"][f"{quote_ticker}{base_ticker}"]) * amount
        return round(result, 3)
