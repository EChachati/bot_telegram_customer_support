from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import database_sql_server as sql_server

# Developer Social Networks
developer_telegram = InlineKeyboardButton(text='Escribele al desarrollador', url="telegram.me/echachati")
developer_github = InlineKeyboardButton(text='GitHub', url="https://github.com/Echachati")
developer_linkedin = InlineKeyboardButton(text='Linkedin', url="https://www.linkedin.com/in/echachati/")
developer_twitter = InlineKeyboardButton(text="Twitter", url="https://www.twitter.com/EJChati")
developer_instagram = InlineKeyboardButton(text='Instagram', url='https://www.instagram.com/echachati/')

# Company social Networks
facebook = InlineKeyboardButton(text='▪  Facebook  ▪', url="facebook.com/masspanve/")
instagram = InlineKeyboardButton(text='▪  Instagram  ▪', url='instagram.com/masspanve/')
whatsapp = InlineKeyboardButton(text='▪  WhatsApp  ▪', url='whatsapp.com/catalog/584127736899/?app_absent=0')
telegram = InlineKeyboardButton(text='▪  Telegram  ▪', url='telegram.me/masspan')

# Command Buttons
location = InlineKeyboardButton(text=' 📍   Ver Ubicación ', callback_data='location')  # TODO
schedule = InlineKeyboardButton(text=' 📆   Ver Horario', callback_data='schedule')
exchange = InlineKeyboardButton(text=' 🏦   Ver Tasa de Cambio', callback_data='exchange')
GPS = InlineKeyboardButton(text='Ir por GPS', url="https://goo.gl/maps/EyY7VMz8bX3MEACF7")

# InlineKeyboardMarkup
keyboard_commands = InlineKeyboardMarkup([
    [location, schedule],
    [exchange]
])

developer_social_networks = InlineKeyboardMarkup([
    [developer_github],
    [developer_linkedin],
    [developer_telegram]
])

social_networks = InlineKeyboardMarkup([
    [telegram],
    [whatsapp],
    [instagram],
    [facebook]
])

# ReplyKeyboardMarkup

menuKeyboard = ReplyKeyboardMarkup([
    ['📍   Ver Ubicación '],
    [' 📆   Ver Horario'],
    [' 🏦   Ver Tasa de Cambio'],
    ['🔍 Buscar Precios'],
    [' 📱 Redes Sociales', ' 📓 Contacta al Desarrollador']
])

pricesKeyboard = ReplyKeyboardMarkup([
    ['Precios Al Mayor'],
    ['Precios Por Categoria'],
    ['Buscar por Mensaje'],
    ['Buscar Por Codigo'],
    ['Volver Al Menu']
])

intancesButtons = []
for k in sql_server.INSTANCES:
    if sql_server.INSTANCES[k] not in [1025, 24, 22, 15]:
        intancesButtons.append([k])
intancesButtons.append(['Volver Al Menu'])

intanceKeyboard = ReplyKeyboardMarkup(intancesButtons)
