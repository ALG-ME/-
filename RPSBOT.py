import telebot
import random
import asyncio
from telebot import types

# Тут токен вашего бота
TOKEN = ''
# Тут вы и сами поняли
bot = telebot.TeleBot(TOKEN)


def send_game_keyboard(chat_id):
    markup = types.InlineKeyboardMarkup()
    rock_button = types.InlineKeyboardButton(text="Камень", callback_data="Камень")
    paper_button = types.InlineKeyboardButton(text="Бумага", callback_data="Бумага")
    scissors_button = types.InlineKeyboardButton(text="Ножницы", callback_data="Ножницы")
    markup.row(rock_button, paper_button, scissors_button)

    bot.send_message(chat_id, "Выберите свой ход:", reply_markup=markup)


@bot.message_handler(commands=['game'])
def game(message):
    send_game_keyboard(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    choices = ['Камень', 'Бумага', 'Ножницы']
    bot_choice = random.choice(choices)

    if call.data in choices:
        player_choice = call.data

        # Логика определения победителя
        if player_choice == bot_choice:
            result = "Ничья!"
        elif (player_choice == 'Камень' and bot_choice == 'Ножницы') or (
                player_choice == 'Бумага' and bot_choice == 'Камень') or (
                player_choice == 'Ножницы' and bot_choice == 'Бумага'):
            result = "Вы победили!"
        else:
            result = "Вы проиграли."

        bot.send_message(call.message.chat.id, f"Ваш выбор: {player_choice}\nВыбор бота: {bot_choice}\n{result}")

        # Удаление клавиатуры после окончания игры
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=None)

    else:
        bot.send_message(call.message.chat.id, "Неверный выбор. Пожалуйста, выберите камень, ножницы или бумагу.")


@bot.message_handler(commands=['start'])
def start(message):
    send_game_keyboard(message.chat.id)


# Запуск обработчика сообщений
bot.infinity_polling()
