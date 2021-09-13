import logging
from telegram import Update, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from src.public.menu.main import constants, buttons
from src.public import exchange

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()

MAIN, PRODUCTS, PAGO_MOVIL = range(3)


def getBotInfo(update: Update, context: CallbackContext) -> int:
    mybot = context.bot
    chat_id = update.message.chat_id
    name = update.effective_user["first_name"]
    last_name = update.effective_user["last_name"]
    username = update.effective_user.username

    logger.info(f'El user {username} ({name}) ha iniciado el bot')

    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=constants.START_INFO(name),
        reply_markup=buttons.social_networks
    )
    update.message.reply_text(
        text="Elige un comando: ", reply_markup=buttons.menuKeyboard)

    return MAIN


def backToMenu(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        text="Volviendo al Menu", reply_markup=buttons.menuKeyboard)
    return MAIN


def getLocation(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(
        f'El user {username} ({name}) le ha pedido la ubicacion al bot')

    update.message.reply_text(text=constants.LOCATION)
    context.bot.sendLocation(
        reply_markup=InlineKeyboardMarkup([[buttons.GPS]]),
        chat_id=update.message.chat_id,
        location=constants.GPS_LOCATION
    )
    return MAIN


def getSchedule(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido el horario al bot')

    context.bot.sendMessage(
        chat_id=update.message.chat_id, text=constants.SCHEDULE, parse_mode="HTML")
    return MAIN


def getExchange(update: Update, context: CallbackContext) -> int:
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(
        f'El user {username} ({name}) le ha pedido la Tasa de Cambio al bot')

    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=exchange.EXCHANGE_VALUE
    )
    return MAIN


def getSocialMedia(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(
        f'El user {username} ({name}) quiere conocer las redes sociales')
    update.message.reply_text(
        "Siguenos en nuestras Redes Sociales",
        reply_markup=buttons.social_networks
    )
    return MAIN


def getDeveloperContact(update: Update, context: CallbackContext) -> int:
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(
        f'El user {username} ({name}) le ha solicitado la información del desarrollador')

    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.DEVELOPER_INFO,
        reply_markup=buttons.developer_social_networks
    )
    return MAIN


def switchToPrices(update: Update, context: CallbackContext) -> int:
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]

    logger.info(f'El user {username} ({name}) Se mueve al menu de precios')
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"Moviendo al Menu precios",
        reply_markup=buttons.pricesKeyboard
    )
    return PRODUCTS


def switchToMobilePayment(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) Desea registrar un Pago Movil')
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f'Inicio registro de Pago Movil',
        reply_markup=ReplyKeyboardMarkup([
            ['Inicio Registro de pago movil'],
            ['Cancelar Registro de pago movil']
        ])
    )

    return PAGO_MOVIL


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("User %s canceled the conversation.", user.first_name)

    return ConversationHandler.END
