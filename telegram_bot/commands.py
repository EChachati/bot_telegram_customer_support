import logging
import os

from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import constants
from telegram_bot.utils import get_barcode

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def getBotInfo(update, context):
    mybot = context.bot
    print(update.message)
    chat_id = update.message.chat_id
    name = update.effective_user["first_name"]
    username = update.effective_user.username
    logger.info(f'El user {username} ({name}) ha iniciado el bot')

    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=constants.START_INFO(name),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=' 📍   Ver Ubicación ', callback_data="ubicacion")],  # TODO Fix
        ])
    )


def getSchedule(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido el horario al bot')
    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.SCHEDULE
    )


def getLocation(update, context):
    # mybot = context.bot
    print(update)
    # chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la ubicacion al bot')

    update.message.reply_text(parse_mode="HTML", text=constants.LOCATION)

    # mybot.sendMessage(
    #    chat_id=chat_id,
    #    parse_mode="HTML",
    #    text="Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente al autolavado, Coro (Venezuela), o <a href='https://www.google.com/maps/dir//11.423235,-69.640745/@11.4251583,-69.6442251,16.27z/data=!4m2!4m1!3e0?hl=es'>Ir por GPS</a> "
    # )


# TODO
def send_location(update, context):    update.message.reply_text(constants.LOCATION, parse_mode='HTML')


def getExchange(update, context):
    mybot = context.bot
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la Tasa de Cambio al bot')
    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=constants.get_exchange_value()
    )


def getContactoDesarrollador(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha solicitado la información del desarrollador')
    button_contacta_al_desarrollador = InlineKeyboardButton(text='Contactar al desarrollador',
                                                            url="telegram.me/echachati")
    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.DEVELOPER_INFO,
        reply_markup=InlineKeyboardMarkup([
            [button_contacta_al_desarrollador],
        ])
    )


def codebarHandler(update, context):
    # Declarate vars
    bot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    file_id = update.message.photo[-1].file_id

    # Download the file
    newFile = bot.getFile(file_id)
    newFile.download('test.jpg')

    # Get the bar code
    code = get_barcode('test.jpg')
    bot.sendMessage(chat_id=update.message.chat_id, text=f"El Código de barras es {code}")
    logger.info(f'El user {username} ({name}) ha enviado un código de barras')

    # Delete the file
    os.remove('test.jpg')
