import telebot
from config import TOKEN, exchanger
from extensions import Converter, APIExceptions

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message: telebot.types.Message):
    text = f"Welcome, {message.chat.username}\nTo get started, enter the command following way\n"
    text += "<currency name> <converted currency> <amount>\n"
    text += "To get list of available currencies type /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def get_values(message: telebot.types.Message):
    bot.send_message(message.chat.id, "loh")
    text = "Available currencies:\n"
    text += "\n".join(f"{i + 1}) {key}" for i, key in enumerate(exchanger.keys()))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def converter(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))
    try:
        result = Converter.get_price(values)
    except APIExceptions as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, e)
    else:
        text = f"{values[2]} {values[0]} = {result} {exchanger[values[1]]}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
