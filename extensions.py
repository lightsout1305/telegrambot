import requests
import json
from config import keys


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException('Нельзя конвертировать одинаковые валюты')

        if int(amount) <= 0:
            raise APIException('Введите количество больше нуля')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        conv = requests.get(f'https://free.currconv.com/api/v7/convert?q='
                            f'{quote_ticker}_{base_ticker}&compact=ultra'
                            f'&apiKey=45eb6038478e4b29cd35')
        total_base = json.loads(conv.content)[f'{quote_ticker}_{base_ticker}']

        return total_base
