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
    # noinspection PyUnboundLocalVariable
    updater = Updater(bot.token, use_context=True)

    # crear despachador
    dispatcher = updater.dispatcher
    # Add Admin Commands
    dispatcher = admin.add_commands(dispatcher)
    # crear comando
    '''
    dispatcher.add_handler(CommandHandler("start", commands.getBotInfo))
    dispatcher.add_handler(CommandHandler("horario", commands.getSchedule))
    dispatcher.add_handler(CommandHandler("ubicacion", commands.getLocation))
    dispatcher.add_handler(CommandHandler("tasaCambio", commands.getExchange))
    dispatcher.add_handler(CommandHandler(
        "contact", commands.getContactoDesarrollador))
    dispatcher.add_handler(CommandHandler("comandos", commands.getAllCommands))
    '''
    # MessageHandlers
    dispatcher.add_handler(MessageHandler(
        Filters.photo, commands.codebarHandler))
    #dispatcher.add_handler(MessageHandler(Filters.text, textHandler))
    '''
    # Callbacks
    dispatcher.add_handler(CallbackQueryHandler(
        commands.getSchedule, pattern='schedule'))
    dispatcher.add_handler(CallbackQueryHandler(
        commands.getExchange, pattern='exchange'))
    dispatcher.add_handler(CallbackQueryHandler(
        commands.getLocation, pattern='location'))
    '''
    dispatcher.add_handler(menu.MenuConversationHandler)

    # Actualization Message
    # actualization_message(bot)

    # Empezar a ejecutar el bot
    # Estar verificando si esta recibiendo mensajes, ponte a vivir y existir
    updater.start_polling()
    updater.idle()  # terminar bot con ctrl+c
