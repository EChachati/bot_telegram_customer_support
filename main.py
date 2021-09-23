########################
# Autor Edkar Chachati #
#   Twitter @EJChati   #
########################

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler

from src.secret import TOKEN
import src.public.commands as commands
from src.public.textHandler import textHandler
from src.utils import actualization_message

from src.public.menu import menuHandler as menu

from src.admin import commands as admin

if __name__ == "__main__":
    # obtener info del bot
    bot = telegram.Bot(token=TOKEN)
    print(bot.getMe())

    # updater se conecta y recibe los mensajes
    updater = Updater(bot.token, use_context=True)

    # Controlador del Bot
    dispatcher.add_handler(menu.MenuConversationHandler)

    # Actualization Message
    # actualization_message(bot)

    # Empezar a ejecutar el bot
    # Estar verificando si esta recibiendo mensajes, ponte a vivir y existir
    updater.start_polling()
    updater.idle()  # terminar bot con ctrl+c
