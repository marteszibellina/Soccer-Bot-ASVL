
import telebot  # type: ignore
from telebot import types
from datetime import datetime
from names import (  # type: ignore
    players,
    players_approved,
    players_denied,
    players_pending,
    players_payed,
    ADMINS,
)
from Menu import (  # type: ignore
    MAIN_MENU_MESSAGE,
    MAIN_BUTTONS,
    INFO,
    ERROR,
    CHECK,
    CONFIRM_BUTTONS,
    CONFIRM_MESSAGE,
    ADMIN_MENU_MESSAGE,
    ADMIN_BUTTONS,
    BACK,
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
        btn1 = types.KeyboardButton(
            MAIN_BUTTONS[0],
        )
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


# Основное меню. Здесь творится магия
@bot.message_handler(content_types=["text"])
def text(mes):
    if mes.text == MAIN_BUTTONS[0]:
        bot.send_message(mes.chat.id, f"{INFO[0]}: \n{game_schedule}")
        bot.send_message(mes.chat.id, f"{INFO[1]}: \n{current_date}")

    elif mes.text == MAIN_BUTTONS[1]:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        btn10 = types.KeyboardButton(CONFIRM_BUTTONS[0])
        btn11 = types.KeyboardButton(CONFIRM_BUTTONS[1])
        btn12 = types.KeyboardButton(CONFIRM_BUTTONS[2])
        btn13 = types.KeyboardButton(BACK)
        keyboard.add(btn10, btn11, btn12, btn13)
        bot.send_message(
            mes.chat.id,
            f"{CONFIRM_MESSAGE[0]}{mes.chat.first_name}",
            reply_markup=keyboard,
        )

    elif mes.text == MAIN_BUTTONS[2]:
        checking(mes)

    elif mes.text == MAIN_BUTTONS[3]:
        bot.send_message(mes.chat.id, f"{INFO[2]}")

    if mes.text == CONFIRM_BUTTONS[0]:
        confirm(mes)
    elif mes.text == CONFIRM_BUTTONS[1]:
        pending(mes)
    elif mes.text == CONFIRM_BUTTONS[2]:
        deny(mes)
    elif mes.text == BACK:
        admin_menu(mes)
    if mes.chat.id in ADMINS.keys():
        admin_button(mes)


@bot.message_handler(func=lambda btn: True)
def checking(mes):
    for mes.chat.id in players.keys():
        if mes.chat.id in players_approved.keys():
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
        elif mes.chat.id in players_pending.keys():
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
        elif mes.chat.id in players_denied.keys():
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
        else:
            bot.send_message(mes.chat.id, f"{CHECK[3]}, {mes.chat.first_name}")


@bot.message_handler(func=lambda btn: True)
def confirm(mes):
    if mes.text == CONFIRM_BUTTONS[0]:
        if mes.chat.id not in players_approved.keys():
            players_approved[mes.chat.id] = mes.chat.first_name
            if (
                mes.chat.id in players_approved.keys()
                and mes.chat.id not in players_pending.keys()
                and mes.chat.id not in players_denied.keys()
            ):
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
            elif (
                mes.chat.id in players_approved.keys()
                and mes.chat.id in players_pending.keys()
                and mes.chat.id not in players_denied.keys()
            ):
                players_pending.pop(mes.chat.id)
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
            elif (
                mes.chat.id in players_approved.keys()
                and mes.chat.id not in players_pending.keys()
                and mes.chat.id in players_denied.keys()
            ):
                players_denied.pop(mes.chat.id)
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")


@bot.message_handler(func=lambda btn: True)
def pending(mes):
    if mes.text == CONFIRM_BUTTONS[1]:
        if mes.chat.id not in players_pending.keys():
            players_pending[mes.chat.id] = mes.chat.first_name
        if (
            mes.chat.id in players_pending.keys()
            and mes.chat.id not in players_approved.keys()
            and mes.chat.id not in players_denied.keys()
        ):
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
        elif (
            mes.chat.id in players_pending.keys()
            and mes.chat.id in players_approved.keys()
            and mes.chat.id not in players_denied.keys()
        ):
            players_approved.pop(mes.chat.id)
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
        elif (
            mes.chat.id in players_approved.keys()
            and mes.chat.id not in players_approved.keys()
            and mes.chat.id in players_denied.keys()
        ):
            players_denied.pop(mes.chat.id)
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
        else:
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")


@bot.message_handler(func=lambda btn: True)
def deny(mes):
    if mes.text == CONFIRM_BUTTONS[2]:
        if mes.chat.id not in players_denied.keys():
            players_denied[mes.chat.id] = mes.chat.first_name
        if (
            mes.chat.id not in players_denied.keys()
            and mes.chat.id not in players_approved.keys()
            and mes.chat.id not in players_pending.keys()
        ):
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
        elif (
            mes.chat.id in players_denied.keys()
            and mes.chat.id in players_approved.keys()
            and mes.chat.id not in players_pending.keys()
        ):
            players_approved.pop(mes.chat.id)
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
        elif (
            mes.chat.id in players_denied.keys()
            and mes.chat.id not in players_approved.keys()
            and mes.chat.id in players_pending.keys()
        ):
            players_pending.pop(mes.chat.id)
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
        else:
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")


@bot.message_handler(func=lambda btn: True)
def admin_button(mes):
    if mes.text == ADMIN_BUTTONS[0]:
        for player_id, player_name in players.items():
            bot.send_message(mes.chat.id, f"{ADMIN_BUTTONS[0]}:\n{player_name}")

    elif mes.text == ADMIN_BUTTONS[1]:
        for player_id, player_name in players_approved.items():
            bot.send_message(mes.chat.id, f"{ADMIN_BUTTONS[1]}:\n{player_name}")

    elif mes.text == ADMIN_BUTTONS[2]:
        for player_id, player_name in players_pending.items():
            bot.send_message(mes.chat.id, f"{ADMIN_BUTTONS[2]}:\n{player_name}")

    elif mes.text == ADMIN_BUTTONS[3]:
        for player_id, player_name in players_denied.items():
            bot.send_message(mes.chat.id, f"{ADMIN_BUTTONS[3]}:\n{player_name}")

    elif mes.text == ADMIN_BUTTONS[4]:
        for player_id, player_name in players_payed.items():
            bot.send_message(mes.chat.id, f"{ADMIN_BUTTONS[4]}:\n{player_name}")


bot.polling(none_stop=True, interval=0)


print("Administrators:", ADMINS)
print("Total players:", players)
print("Approved Players:", players_approved)
print("Pending Players", players_pending)
print("Denied Players:", players_denied)
print("Payed Players", players_payed)
