import datetime

admins = {'Dmitry': 3568804, 'Виталий': 1201661895}
players = {}
players_approved = []
players_denied = []
players_pending = []
players_payed = []

def clear_players():
    if datetime.now().strftime("%d.%m.%Y") == datetime.date.isoweekday("Четверг"):
        players_approved = []
        players_denied = []
        players_pending = []
        players_payed = []
    else:
        pass
    return players_approved, players_denied, players_pending, players_payed

