import logging

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler,    CommandHandler,    MessageHandler,    Filters
from src.public.menu.main.commands import *
from src.public.menu.main import textHandler as main
from src.states import *
import src.public.menu.mobilePayment as pm
from src.admin.menu import handler as admin
from src.admin.menu import commands as adminCommands
from src.public.product import handler as product
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


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
            MessageHandler(Filters.text, main.textHandler),
            CommandHandler('admin', adminCommands.menu)
        ],
        PRODUCTS: [
            product.handler
        ],
        PAGO_MOVIL: [
            pm.handler
        ],
        ADMIN: [
            MessageHandler(Filters.text, admin.textHandler)
        ]
    },
    fallbacks=[CommandHandler('cancelar', cancel)],
    allow_reentry=True,

)
