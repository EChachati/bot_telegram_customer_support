from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
# Command Buttons
location = InlineKeyboardButton(
    text=' 📍   Ver Ubicación ', callback_data='location')  # TODO
schedule = InlineKeyboardButton(
    text=' 📆   Ver Horario', callback_data='schedule')
exchange = InlineKeyboardButton(
    text=' 🏦   Ver Tasa de Cambio', callback_data='exchange')

# InlineKeyboardMarkup
keyboard_commands = InlineKeyboardMarkup([
    [location, schedule],
    [exchange]
])


# ReplyKeyboardMarkup

pricesKeyboard = ReplyKeyboardMarkup([
    ['Precios Al Mayor'],
    ['Precios Por Categoria'],
    ['Buscar por Mensaje'],
    ['Buscar Por Codigo'],
    ['Volver Al Menu']
])

"""
BANNED WHILE NOT DB
intancesButtons = []
for k in sql_server.INSTANCES:
    if sql_server.INSTANCES[k] not in [1025, 24, 22, 15]:
        intancesButtons.append([k])
intancesButtons.append(['Volver Al Menu'])

intanceKeyboard = ReplyKeyboardMarkup(intancesButtons)
"""
