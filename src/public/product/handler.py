from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters
)

from src.public.product.commands import *
from src.public.product.codebarHandler import (
    codebarImageHandler,
    codebarTextHandler
)
from src.states import *

handler = ConversationHandler(
    entry_points=[
        MessageHandler(
            Filters.regex('🔍 Buscar Precios'),
            price_type
        ),
        MessageHandler(Filters.regex('Precio Regular'), price_type),
        MessageHandler(Filters.regex('Precio al por Mayor'), price_type)

    ],

    states={
        PRICE_TYPE: [
            MessageHandler(Filters.text, search_type)
        ],
        SEARCH_CAT: [
            MessageHandler(Filters.text, categoryHandler)
        ],
        SEARCH_CODE: [
            MessageHandler(Filters.photo, codebarImageHandler),
            MessageHandler(Filters.text, codebarTextHandler)
        ],
        SEARCH_NAME: [
            MessageHandler(Filters.text, searchByName)
        ],
    },
    fallbacks=[
        MessageHandler(Filters.regex(
            'Volver al Menu Principal'), cancel)
    ],
    map_to_parent={
        MAIN: MAIN
    }


)
