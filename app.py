import telebot
from config import TOKEN, exchanger
from extensions import Converter, APIExceptions, UserDB

bot = telebot.TeleBot(TOKEN)
db = UserDB()

def_conv = {
    1: ("USD", "RUB")
}


@bot.message_handler(commands=["start", "help"])
def send_welcome(message: telebot.types.Message):
    text = f"Welcome, {message.chat.username}\nTo get started, enter the command following way\n"
    text += "/values To get list of available currencies\n"
    text += "/set For setting converted currencies with buttons\n"
    text += "Default conversion is USD -> RUB"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def get_values(message: telebot.types.Message):
    bot.send_message(message.chat.id, "loh")
    text = "Available currencies:\n"
    text += "\n".join(f"{i + 1}) {key}" for i, key in enumerate(exchanger.keys()))
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["set"])
def setter(message: telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup()
    for cur, ticker in exchanger.items():
        button = telebot.types.InlineKeyboardButton(text=cur.capitalize(), callback_data=f"cur1 {ticker}")
        markup.add(button)
    bot.send_message(message.chat.id, text="Choose base currency", reply_markup=markup)

    markup = telebot.types.InlineKeyboardMarkup()
    for cur, ticker in exchanger.items():
        button = telebot.types.InlineKeyboardButton(text=cur.capitalize(), callback_data=f"cur2 {ticker}")
        markup.add(button)
    bot.send_message(message.chat.id, text="Choose quote currency", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    cur_pos, cur = call.data.split()
    user_id = call.message.chat.id
    if cur_pos == "cur1":
        db.change_from(user_id, cur)
    if cur_pos == "cur2":
        db.change_to(user_id, cur)

    pair = db.get_pair(user_id)
    bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                              text=f"Now convert from {pair[0]} to {pair[1]}")


@bot.message_handler(content_types=["text"])
def converter(message: telebot.types.Message):
    pair = db.get_pair(message.chat.id)
    values = [*pair, message.text.strip()]
    try:
        result = Converter.get_price(values)
    except APIExceptions as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, e)
    else:
        text = f"{values[2]} {values[0]} = {result} {values[1]}"
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True, interval=0)
