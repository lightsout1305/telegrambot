from environs import Env

env = Env()

env.read_env(".env")

TOKEN = env.str("TOKEN")

keys = {'доллар': 'USD',
        'евро': 'EUR',
        'рубль': 'RUB'}
