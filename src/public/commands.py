import logging
import os

from telegram import InlineKeyboardMarkup

import src.public.buttons as buttons
#import src.constants as constants

# Banned DBs
#import database.mysql.database_mysql as mysql
#import database.sqlserver.database_sql_server as sql_server
from src.utils import get_barcode, add_to_unknown_messages, formated_product_list

global photo_id
photo_id = 0

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def codebarHandler(update, context):
    # Declarate vars
    global photo_id
    bot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    file_id = update.message.photo[-1].file_id
    chat_id = update.message.chat_id

    # Download the file
    newFile = bot.getFile(file_id)
    newFile.download(f'{photo_id}.jpg')

    # Get the bar code
    code = get_barcode(f'{photo_id}.jpg')

    if code == 'inlegible':
        bot.sendMessage(chat_id=chat_id, text=f"El Código de barras es {code}")
        logger.info(
            f'El user {username} ({name}) ha enviado un código de barras {code}')
        mysql.add_log_to_db(update.message.chat_id,
                            f'El user {username} ({name})  ha enviado un código de barras {code}')
        photo_id += 1
    else:
        logger.info(
            f'El user {username} ({name}) ha enviado un código de barras')
        product = sql_server.search_product_by_barcode(code)
        if product == {}:
            bot.sendMessage(
                chat_id=chat_id, text=f"El producto con el código de barras '{code}' no existe")
            photo_id += 1
            mysql.add_log_to_db(chat_id=chat_id,
                                text=f"El User {username} ({name}) busco un producto que no existe '{code}'")
        else:
            # Delete the file
            price = product['detal'] * constants.DOLAR_FLOAT
            os.remove(f'{photo_id}.jpg')
            bot.sendMessage(chat_id=chat_id,
                            text=f"{product['description']}\nAproximadamente Bs. {price:,.2f}")
            logger.info(
                f'El user {username} ({name}) ha recibido el precio del producto {product["description"]} Bs. {price:,.2f}')
            mysql.add_log_to_db(update.message.chat_id,
                                f'El user {username} ({name}) ha recibido el precio del producto {product["description"]} Bs. {price:,.2f}')


def getAllCommands(update, context):
    bot = context.bot

    bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"Todos nuestros comandos son:",
        reply_markup=InlineKeyboardMarkup([
            [buttons.location],
            [buttons.exchange],
            [buttons.schedule]
        ])
    )


def switch_to_prices_keyboard(update, context):
    logger.info(f'El user {username} ({name}) Se mueve al menu de precios')
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"Moviendo al Menu precios",
        reply_markup=buttons.pricesKeyboard
    )
