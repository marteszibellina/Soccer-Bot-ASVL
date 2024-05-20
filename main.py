import telebot
from telebot import types
from datetime import datetime
from names import (
    players,
    players_approved,
    players_denied,
    players_pending,
    players_payed,
    ADMINS,
)
from Menu import (
    MAIN_MENU_MESSAGE,
    MAIN_BUTTONS,
    INFO,
    MENUS,
    CHECK,
    CONFIRM_BUTTONS,
    CONFIRM_MESSAGE,
    ADMIN_MENU_MESSAGE,
    ADMIN_BUTTONS,
    BACK,
    ERROR,
    MENU_LIST,
)

token = "6877818588:AAHK_9cdOuYSLmuINO-TD2pOGVH0wweyDmo"
bot = telebot.TeleBot(token)

game_schedule = "Среда, 19:00 - 22:00"
weekday = [
    "Понедельник",
    "Вторник",
    "Среда",
    "Четверг",
    "Пятница",
    "Суббота",
    "Воскресенье",
]
current_date = datetime.now().strftime("%d.%m.%Y")
current_weekday = weekday[datetime.now().weekday()]

# Главное меню. При запуске бота будет высвечиваться приветственное сообщение


@bot.message_handler(commands=["start"])
def admin_menu(mes):
    bot.send_message(
        mes.chat.id,
        f"Привет, {mes.chat.first_name}! Я твой персональный помощник!",
    )
    if mes.chat.id not in players.keys():
        players[mes.chat.id] = mes.chat.first_name
    if mes.chat.id in ADMINS.keys():
        bot.send_message(
            mes.chat.id,
            f"{mes.chat.first_name}, {ADMIN_MENU_MESSAGE[2]}",
        )
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn1 = types.KeyboardButton(MAIN_BUTTONS[0])
        btn2 = types.KeyboardButton(MAIN_BUTTONS[1])
        btn3 = types.KeyboardButton(MAIN_BUTTONS[2])
        btn4 = types.KeyboardButton(MAIN_BUTTONS[3])
        btn5 = types.KeyboardButton(ADMIN_BUTTONS[0])
        btn6 = types.KeyboardButton(ADMIN_BUTTONS[1])
        btn7 = types.KeyboardButton(ADMIN_BUTTONS[2])
        btn8 = types.KeyboardButton(ADMIN_BUTTONS[3])
        btn9 = types.KeyboardButton(ADMIN_BUTTONS[4])
        keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)
        bot.send_message(mes.chat.id, f"{ADMIN_MENU_MESSAGE[0]}")
        bot.send_message(
            mes.chat.id,
            f"{ADMIN_MENU_MESSAGE[1]}",
            reply_markup=keyboard,
        )
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
        btn1 = types.KeyboardButton(MAIN_BUTTONS[0])
        btn2 = types.KeyboardButton(MAIN_BUTTONS[1])
        btn3 = types.KeyboardButton(MAIN_BUTTONS[2])
        btn4 = types.KeyboardButton(MAIN_BUTTONS[3])
        keyboard.add(btn1, btn2, btn3, btn4)
        bot.send_message(mes.chat.id, f"{MAIN_MENU_MESSAGE[0]}")
        bot.send_message(
            mes.chat.id,
            f"{MAIN_MENU_MESSAGE[1]}",
            reply_markup=keyboard,
        )


# Функция главного меню. Основное. Из этого меню можно попасть в следующие


@bot.message_handler(content_types=["text"])
for number in MENU_LIST:
    if number == 8:
        def return_back(mes):
            main_menu(mes)

    if number == 8:
        def check_in_confirm(mes):
            for mes.chat.id in players.keys():
                if mes.chat.id in players_approved:
                    bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
                elif mes.chat.id in players_pending:
                    bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
                elif mes.chat.id in players_denied:
                    bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
                else:
                    bot.send_message(mes.chat.id, f"{CHECK[3]}")

    if number == 7:
        def clear_lists(mes):
            if mes.chat.id in players_approved:
                players_pending.remove(mes.chat.id)
                players_denied.remove(mes.chat.id)
            elif mes.chat.id in players_pending:
                players_approved.remove(mes.chat.id)
                players_denied.remove(mes.chat.id)
            elif mes.chat.id in players_denied:
                players_approved.remove(mes.chat.id)
                players_pending.remove(mes.chat.id)
            else:
                bot.send_message(mes.chat.id, "Fffuuuck!")

    if number == 6:
        def check_in_main(mes):
            bot.send_message(mes.chat.id, f"{MENUS[1]}")
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            btn10 = types.KeyboardButton(CONFIRM_BUTTONS[0])
            btn11 = types.KeyboardButton(CONFIRM_BUTTONS[1])
            btn12 = types.KeyboardButton(CONFIRM_BUTTONS[2])
            btn13 = types.KeyboardButton(BACK)
            keyboard.add(btn10, btn11, btn12, btn13)
            bot.send_message(
                mes.chat.id,
                f"{CONFIRM_MESSAGE[0]}{mes.chat.first_name}?",
                reply_markup=keyboard,
            )

    if number == 5:
        def confirm(mes):
            for mes.chat.id in players.keys():
                if mes.chat.id not in players_approved and mes.chat.id in players.keys():
                    players_approved[mes.chat.id] = mes.chat.first_name
                clear_lists(mes)
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
            else:
                bot.send_message(mes.chat.id, f"{ERROR[2]}")
            return_back(mes)

def pending(mes):
    if mes.text == CONFIRM_BUTTONS[1]:
        for mes.chat.id in players.keys():
    if mes.chat.id not in players_pending:
        players_pending[mes.chat.id] = mes.chat.first_name
        clear_lists(mes)
        bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
    return_back(mes)


def deny(mes):
    if mes.text == CONFIRM_BUTTONS[2]:
        for mes.chat.id in players.keys():
            if mes.chat.id not in players_denied:
                players_denied[mes.chat.id] = mes.chat.first_name
                clear_lists(mes)
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
    return_back(mes)


def confirmation(mes):
    if mes.text == CONFIRM_BUTTONS[0]:
        confirm(mes)
    elif mes.text == CONFIRM_BUTTONS[1]:
        pending(mes)
    elif mes.text == CONFIRM_BUTTONS[2]:
        deny(mes)
    elif mes.text == BACK:
        return_back(mes)
    else:
        bot.send_message(mes.chat.id, f"{ERROR[1]}")


def main_menu(mes):
    bot.send_message(mes.chat.id, f"{MENUS[0]}")
    if mes.text == MAIN_BUTTONS[0]:
        bot.send_message(mes.chat.id, f"{INFO[0]}: \n{game_schedule}")
        bot.send_message(mes.chat.id, f"{INFO[1]}: \n{current_date}")
    elif mes.text == MAIN_BUTTONS[1]:
        check_in_main(mes)
    elif mes.text == MAIN_BUTTONS[2]:
        check_in_confirm(mes)
    elif mes.text == MAIN_BUTTONS[3]:
        bot.send_message(mes.chat.id, f"{INFO[2]}")
    else:
        bot.send_message(mes.chat.id, f"{ERROR[0]}")


bot.polling(none_stop=True, interval=0)


print("Administrators:", ADMINS)
print("Total players:", players)
print("Approved Players:", players_approved)
print("Pending Players", players_pending)
print("Denied Players:", players_denied)
print("Payed Players", players_payed)
