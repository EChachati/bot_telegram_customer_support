import logging

from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    Filters
)

from src.states import *
from src.admin.menu.commands import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def textHandler(update: Update, context: CallbackContext):
    print('handler')
    command_dict = {
        'Obtener Ultimos Pago Movil': getPM,
        'Pago Movil Confirmados': getConfirmedPM,
        'Pago Movil Sin Confirmar': getUnconfirmedPM,
        'Registros No Encontrados': recordsNotFounds,
        'Total pago Movil (Mes)': totalPM,
        'Volver Al Menu Anterior': backToMenu
    }
    text = update.message['text']
    if text in command_dict.keys():
        return command_dict[text](update, context)


handler = ConversationHandler(
    entry_points=[
        CommandHandler('admin', menu),
        MessageHandler(Filters.regex(
            'Confirmar Entrada a Modo Admin'), menu),
        MessageHandler(Filters.regex('Admin'), menu),
        MessageHandler(
            Filters.regex('Cancelar Entrada a Modo Admin'), backToMenu)

    ],
    states={
        ADMIN_PM: [
            MessageHandler(Filters.text, textHandler)
        ]
    },
    fallbacks=[
        MessageHandler(Filters.regex('Volver Al Menu Anterior'), backToMenu)
    ],
    map_to_parent={
        MAIN: MAIN
    }
)
