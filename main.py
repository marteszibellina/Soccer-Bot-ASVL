import telebot
from telebot import types
from datetime import datetime
from names import players, players_approved, players_denied, players_pending, players_payed
from schedule import game_schedule

token = "6877818588:AAHNKsoxApn51aelncytFGCMOwVkoHYhKJA"
bot = telebot.TeleBot(token)

weekday = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
current_date = datetime.now().strftime("%d.%m.%Y")
current_weekday = weekday[datetime.now().weekday()]


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я твой персональный помощник!")
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    btn1 = types.KeyboardButton("Когда игра?")
    btn2 = types.KeyboardButton("Записаться")
    btn3 = types.KeyboardButton("Я записан?")
    btn4 = types.KeyboardButton("Контакты")
    keyboard.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, "Выбери интересующую тебя опцию", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "Когда игра?":
        bot.send_message(message.chat.id, f"Сегодня: \n{current_date} \n{current_weekday}")
        bot.send_message(message.chat.id, f"Игра: \n{game_schedule}")
    elif message.text == "Записаться":
        for player in players:
            if player not in players_approved:
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                btn5 = types.KeyboardButton("Да, записывай")
                btn6 = types.KeyboardButton("Не уверен")
                btn7 = types.KeyboardButton("Нет, отказываюсь")
                keyboard.add(btn5, btn6, btn7)
                bot.send_message(message.chat.id, f"Ты уверен, {player}?", reply_markup=keyboard)
    elif message.text == "Я записан?":
        for player in players:
            if player in players_pending:
                bot.send_message(message.chat.id, f"{player}, ты в сомнениях.")
            elif player in players_approved:
                bot.send_message(message.chat.id, f"{player}, ты в игре.")
            elif player in players_denied:
                bot.send_message(message.chat.id, f"{player}, ты вне игры.")
    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "Контакты:"
                                          "@ArtStudioVitaliyaLeshchenko")
    else:
        bot.send_message(message.chat.id, "Неизвестная команда")
    if message.text == "Да, записывай":
        for player in players:
            if player not in players_approved:
                players_approved.append(player)
                bot.send_message(message.chat.id, f"{player}, ты в игре.")
    elif message.text == "Не уверен":
        for player in players:
            if player not in players_pending:
                players_pending.append(player)
                bot.send_message(message.chat.id, f"{player}, ты в сомнениях.")
    elif message.text == "Нет, отказываюсь":
        for player in players:
            if player not in players_denied:
                players_denied.append(player)
                bot.send_message(message.chat.id, f"{player}, ты вне игры.")


bot.polling(none_stop=True, interval=0)

