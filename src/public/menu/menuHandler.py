import logging

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler,    CommandHandler,    MessageHandler,    Filters
from src.public.menu.main.commands import *
from src.public.menu.main import textHandler as main

import src.public.menu.mobilePayment as pm

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()

MAIN, PRODUCTS, PAGO_MOVIL = range(3)


def mainMenuMessageHandler(update, context):
    text = update.message['text']


MenuConversationHandler = ConversationHandler(
    entry_points=[
        CommandHandler('start', getBotInfo),
        MessageHandler(Filters.regex(
            'Volver Al Menu'), backToMenu)
    ],
    states={
        MAIN: [
            MessageHandler(Filters.text, main.textHandler)
        ],
        PRODUCTS: [

        ],
        PAGO_MOVIL: [
            pm.handler
        ]
    },
    fallbacks=[CommandHandler('cancelar', cancel)]

)
