import logging
import os

from telegram import InlineKeyboardMarkup

import constants
import database_mysql as sql
from src import buttons
from src.utils import get_barcode, add_to_unknown_messages

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def getBotInfo(update, context):
    mybot = context.bot
    print(update.message)
    chat_id = update.message.chat_id
    name = update.effective_user["first_name"]
    last_name = update.effective_user["last_name"]
    username = update.effective_user.username
    logger.info(f'El user {username} ({name}) ha iniciado el bot')

    if not sql.is_active_user(chat_id):
        sql.insert_user(chat_id=chat_id, username=username, first_name=name, last_name=last_name)

    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=constants.START_INFO(name),
        reply_markup=buttons.social_networks
    )
    update.message.reply_text(text="Elige un comando: ", reply_markup=buttons.replyKeyboard)


def getSchedule(update, context):
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido el horario al bot')
    try:
        context.bot.sendMessage(text=constants.SCHEDULE, parse_mode="HTML")
    except:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=constants.SCHEDULE, parse_mode='HTML')


def getLocation(update, context):
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la ubicacion al bot')

    try:
        update.message.reply_text(text=constants.LOCATION)
        context.bot.sendLocation(
            reply_markup=InlineKeyboardMarkup([[buttons.GPS]]),
            chat_id=update.message.chat_id,
            location=constants.gps_location)
    except:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=constants.LOCATION, reply_markup=InlineKeyboardMarkup([[buttons.GPS]]))


def getExchange(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la Tasa de Cambio al bot')
    try:
        mybot.sendMessage(
            chat_id=update.message.chat_id,
            parse_mode="HTML",
            text=constants.EXCHANGE_VALUE
        )
    except:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=constants.EXCHANGE_VALUE, parse_mode='HTML')


def getContactoDesarrollador(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha solicitado la información del desarrollador')

    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.DEVELOPER_INFO,
        reply_markup=buttons.developer_social_networks
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


def textHandler(update, context):
    # Declarate vars
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    text = (update.message['text'])

    if text == '📍   Ver Ubicación':
        getLocation(update, context)
    elif text == '📆   Ver Horario':
        getSchedule(update, context)
    elif text == '🏦   Ver Tasa de Cambio':
        getExchange(update, context)
    elif text == '🔍 Ver Codigo de Barras':
        logger.info(f'El user {username} ({name}) quiere revisar un código de barras')
        update.message.reply_text("Envianos una foto nitida del código de barras a analizar")
    elif text == '📱 Redes Sociales':
        logger.info(f'El user {username} ({name}) quiere conocer las redes sociales')
        update.message.reply_text("Siguenos en nuestras Redes Sociales", reply_markup=buttons.social_networks)
    elif text == '📓 Contacta al Desarrollador':
        getContactoDesarrollador(update, context)
    else:
        unexcepted_command = (f'{username}({name}) send "{text}" is not a command')
        logger.info(unexcepted_command)
        add_to_unknown_messages(unexcepted_command)
