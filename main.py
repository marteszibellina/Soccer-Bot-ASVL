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
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}! Я твой персональный помощник!")
    if message.chat.first_name not in players.keys() and message.chat.id not in players.items():
        players[message.chat.first_name] = message.chat.id
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn1 = types.KeyboardButton("Когда игра?")
        btn2 = types.KeyboardButton("Записаться")
        btn3 = types.KeyboardButton("Я записан?")
        btn4 = types.KeyboardButton("Контакты")
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Главное меню. \nВыбери интересующую тебя опцию", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "Когда игра?":
        bot.send_message(message.chat.id, f"Игра: \n{game_schedule}")
        bot.send_message(message.chat.id, f"А сегодня: \n{current_weekday}, {current_date}")
    elif message.text == "Записаться":
        for player in players:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            btn5 = types.KeyboardButton("Да, записывай")
            btn6 = types.KeyboardButton("Не уверен")
            btn7 = types.KeyboardButton("Нет, отказываюсь")
            btn8 = types.KeyboardButton("Назад")
            keyboard.add(btn5, btn6, btn7, btn8)
            bot.send_message(message.chat.id, f"Ты уверен, {player}?", reply_markup=keyboard)
    elif message.text == "Я записан?":
        for player in players:
            if player in players_pending:
                bot.send_message(message.chat.id, f"{player}, ты в сомнениях.")
            elif player in players_approved:
                bot.send_message(message.chat.id, f"{player}, ты в игре.")
            elif player in players_denied:
                bot.send_message(message.chat.id, f"{player}, ты вне игры.")
            else:
                bot.send_message(message.chat.id, f"{player}, информация не найдена.")
    elif message.text == "Контакты":
        bot.send_message(message.chat.id, "Контакты:\n"
                                          "@ArtStudioVitaliyaLeshchenko")
    if message.text == "Да, записывай":
        for player in players:
            if player not in players_approved:
                players_approved.append(player)
                bot.send_message(message.chat.id, f"{player}, ты в игре.")
                if player in players_approved and player not in players_pending and player not in players_denied:
                    continue
                elif player in players_approved and player in players_pending and player not in players_denied:
                    players_pending.remove(player)
                elif player in players_approved and player not in players_pending and player in players_denied:
                    players_denied.remove(player)
        def back(message, bot):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            btn1 = types.KeyboardButton("Когда игра?")
            btn2 = types.KeyboardButton("Записаться")
            btn3 = types.KeyboardButton("Я записан?")
            btn4 = types.KeyboardButton("Контакты")
            keyboard.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Главное меню. \nВыбери интересующую тебя опцию", reply_markup=keyboard)
        back(message, bot)
    elif message.text == "Не уверен":
        for player in players:
            if player not in players_pending:
                players_pending.append(player)
                bot.send_message(message.chat.id, f"{player}, ты в сомнениях.")
                if player in players_pending and player not in players_approved and player not in players_denied:
                    continue
                elif player in players_pending and player in players_approved and player not in players_denied:
                    players_approved.remove(player)
                elif player in players_pending and player not in players_approved and player in players_denied:
                    players_denied.remove(player)
        def back(message, bot):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            btn1 = types.KeyboardButton("Когда игра?")
            btn2 = types.KeyboardButton("Записаться")
            btn3 = types.KeyboardButton("Я записан?")
            btn4 = types.KeyboardButton("Контакты")
            keyboard.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Главное меню. \nВыбери интересующую тебя опцию", reply_markup=keyboard)
        back(message, bot)
    elif message.text == "Нет, отказываюсь":
        for player in players:
            if player not in players_denied:
                players_denied.append(player)
                bot.send_message(message.chat.id, f"{player}, ты вне игры.")
                if player in players_denied and player not in players_approved and player not in players_pending:
                    continue
                elif player in players_denied and player in players_approved and player not in players_pending:
                    players_approved.remove(player)
                elif player in players_denied and player not in players_approved and player in players_pending:
                    players_pending.remove(player)
        def back(message, bot):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            btn1 = types.KeyboardButton("Когда игра?")
            btn2 = types.KeyboardButton("Записаться")
            btn3 = types.KeyboardButton("Я записан?")
            btn4 = types.KeyboardButton("Контакты")
            keyboard.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Главное меню. \nВыбери интересующую тебя опцию", reply_markup=keyboard)
        back(message, bot)
    elif message.text == "Назад":
        def back(message, bot):
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            btn1 = types.KeyboardButton("Когда игра?")
            btn2 = types.KeyboardButton("Записаться")
            btn3 = types.KeyboardButton("Я записан?")
            btn4 = types.KeyboardButton("Контакты")
            keyboard.add(btn1, btn2, btn3, btn4)
            bot.send_message(message.chat.id, "Главное меню. \nВыбери интересующую тебя опцию", reply_markup=keyboard)
        back(message, bot)


bot.polling(none_stop=True, interval=0)

print("Total players:", players)
print("Approved Players:", players_approved)
print("Pending Players", players_pending)
print("Denied Players:", players_denied)
print("Payed Players", players_payed)