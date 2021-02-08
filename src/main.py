########################
# Autor Edkar Chachati #
#   Twitter @EJChati   #
########################

import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from src import commands
from secret import TOKEN

if __name__ == "__main__":
    # obtener info del bot
    bot = telegram.Bot(token=TOKEN)
    print(bot.getMe())

    # updater se conecta y recibe los mensajes
    # noinspection PyUnboundLocalVariable
    updater = Updater(bot.token, use_context=True)

    # crear despachador
    dispatcher = updater.dispatcher

    # crear comando
    dispatcher.add_handler(CommandHandler("start", commands.getBotInfo))
    dispatcher.add_handler(CommandHandler("horario", commands.getSchedule))
    dispatcher.add_handler(CommandHandler("ubicacion", commands.getLocation))
    dispatcher.add_handler(CommandHandler("tasaCambio", commands.getExchange))
    dispatcher.add_handler(CommandHandler("contact", commands.getContactoDesarrollador))

    dispatcher.add_handler(MessageHandler(Filters.photo, commands.codebarHandler))

    # Empezar a ejecutar el bot
    updater.start_polling()  # Estar verificando si esta recibiendo mensajes, ponte a vivir y existir
    updater.idle()  # terminar bot con ctrl+c
