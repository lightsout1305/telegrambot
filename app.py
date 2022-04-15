import telebot

from config import *
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = "Чтобы конвертировать валюты, введите следующие команды:\n<имя валюты, цену которой вы хотите узнать> " \
           "<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n" \
           "Чтобы увидеть все доступные валюты, введите /currency"
    bot.reply_to(message, text)


@bot.message_handler(commands=['currency'])
def currency(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Укажите 3 параметра')

        quote, base, amount = values
        quote, base = quote.lower(), base.lower()

        total_base = CurrencyConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}.')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}.')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base * int(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
