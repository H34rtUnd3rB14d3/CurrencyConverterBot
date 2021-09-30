import telebot

TOKEN = "2026535467:AAGSImDBSKFBU5akKqmGFW1EWxT2pOMBYRE"

bot = telebot.TeleBot(TOKEN)

values = {
    "dollar": "USD",
    "euro": "EUR"
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = f"Welcome, {message.chat.username}\nTo get started, enter the command following way\n"
    text += "<currency name> <converted currency> <amount>\n"
    text += "To get list of available currencies type /values"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def get_values(message):
    text = "Available currencies:"
    for keys in values.keys():
        text += f"\n{keys}"
    bot.send_message(message, text)


bot.polling(none_stop=True)
