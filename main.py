import telebot  # type: ignore
from telebot import types
from names import *  # type: ignore
from Menu import *  # type: ignore
from settings import *  # type: ignore
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("log_1")

bot = telebot.TeleBot(token)  # type: ignore

current_date = datetime.now().strftime("%d.%m.%Y")  # type: ignore
current_weekday = weekday[datetime.now().weekday()]  # type: ignore

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
        btn5 = types.KeyboardButton(ADMIN_BUTTONS[5])
        keyboard.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(mes.chat.id, f"{ADMIN_MENU_MESSAGE[0]}")
        bot.send_message(
            mes.chat.id,
            f"{ADMIN_MENU_MESSAGE[1]}",
            reply_markup=keyboard,
        )
    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
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
        bot.send_message(
            mes.chat.id,
            f"{INFO[0]}: \n{game_schedule}",
        )
        bot.send_message(mes.chat.id, f"{INFO[1]}: \n{current_weekday}, {current_date}")

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
        if mes.chat.id in players_approved.keys():
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
        elif mes.chat.id in players_pending.keys():
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[1]}")
        elif mes.chat.id in players_denied.keys():
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
        else:
            bot.send_message(mes.chat.id, f"{CHECK[3]}, {mes.chat.first_name}")

    elif mes.text == MAIN_BUTTONS[3]:
        bot.send_message(mes.chat.id, f"{INFO[2]}")

    elif mes.text == ADMIN_BUTTONS[5]:
        bot.send_message(
            mes.chat.id,
            f"{ADMIN_BUTTONS[0]}: \n{players}"
            f"\n{ADMIN_BUTTONS[1]}: \n{players_approved}"
            f"\n{ADMIN_BUTTONS[2]}: \n{players_pending}"
            f"\n{ADMIN_BUTTONS[3]}: \n{players_denied}"
            f"\n{ADMIN_BUTTONS[4]}: \n{players_payed} rub",
        )

    if mes.text == CONFIRM_BUTTONS[0]:
        confirm(mes)
    elif mes.text == CONFIRM_BUTTONS[1]:
        pending(mes)
    elif mes.text == CONFIRM_BUTTONS[2]:
        deny(mes)
    elif mes.text == BACK:
        admin_menu(mes)


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
                players_payed[0] += price
            elif (
                mes.chat.id in players_approved.keys()
                and mes.chat.id in players_pending.keys()
                and mes.chat.id not in players_denied.keys()
            ):
                players_pending.pop(mes.chat.id)
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
                players_payed[0] += price
            elif (
                mes.chat.id in players_approved.keys()
                and mes.chat.id not in players_pending.keys()
                and mes.chat.id in players_denied.keys()
            ):
                players_denied.pop(mes.chat.id)
                bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[0]}")
                players_payed[0] += price
    admin_menu(mes)


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
    admin_menu(mes)


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
            players_payed[0] -= price
        elif (
            mes.chat.id in players_denied.keys()
            and mes.chat.id in players_approved.keys()
            and mes.chat.id not in players_pending.keys()
        ):
            players_approved.pop(mes.chat.id)
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
            players_payed[0] -= price
        elif (
            mes.chat.id in players_denied.keys()
            and mes.chat.id not in players_approved.keys()
            and mes.chat.id in players_pending.keys()
        ):
            players_pending.pop(mes.chat.id)
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
            players_payed[0] -= price
        else:
            bot.send_message(mes.chat.id, f"{mes.chat.first_name}{CHECK[2]}")
    admin_menu(mes)


bot.polling(none_stop=True, interval=0)


print("Administrators:", ADMINS)  # type: ignore
print("Total players:", players)  # type: ignore
print("Approved Players:", players_approved)  # type: ignore
print("Pending Players", players_pending)  # type: ignore
print("Denied Players:", players_denied)  # type: ignore
print(f"Total amount from players must be: {players_payed} rub")  # type: ignore
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
