import logging
import os

from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

from datetime import datetime

from src.public.menu.main import buttons
from sheets import utils as sheets

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()
MAIN, PRODUCTS, PAGO_MOVIL = range(3)
REF, AMOUNT, PHONE = range(3, 6)


def get_ref(update: Update, context: CallbackContext) -> int:
    if update.message.text == 'Cancelar Registro de pago movil':
        logger.info("User %s canceled the conversation.",
                    update.effective_user['first_name'])
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Ha cancelado el registro del Pago Móvil',
            reply_markup=buttons.menuKeyboard)
        return MAIN
    else:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='¡Hola! Veo que quieres registrar un pago móvil hecho a nosotros, por favor envia el número de referencia :)',
            reply_markup=ReplyKeyboardRemove()
        )

    return REF


def get_amount(update: Update, context: CallbackContext) -> int:
    context.user_data['reference'] = update.message.text
    if update.message.text == 'Cancelar Registro de pago movil':
        return cancel(update, context)
    else:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='¡Bien! Ahora ingresa el monto que transferiste, usa el siguente formato en el mensaje: 1234567.89  (Envia solo el número)',
            reply_markup=ReplyKeyboardRemove()
        )
    return AMOUNT


def get_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['amount'] = update.message.text
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text='¡Buenisimo! Finalmente envianos un número de teléfono para contactarte en caso de ser necesario',
        reply_markup=ReplyKeyboardRemove()
    )
    return PHONE


def end_payment(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text

    date = datetime.now().strftime('%d/%m/%Y')
    phone = context.user_data['phone']
    amount = context.user_data['amount']
    reference = context.user_data['reference']
    chat_id = update.message.chat.id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    data = [date, chat_id, username, first_name,
            last_name, phone, reference, amount]

    sheet = sheets.getGoogleSpreadsheet(
        sheets.GOOGLE_CREDENTIALS,
        sheets.ACCOUNT_STATE_SHEET_KEY
    )
    sh = sheet.worksheet('TLG Pago Movil').append_row(data)
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Perfecto! Ha sido registrado, en caso de algún problema, nuestro equipo se comunicará con usted\n¡Mass Sabor con Mass Pan!',
        reply_markup=buttons.menuKeyboard)
    return MAIN


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("User %s canceled the conversation.",
                update.effective_user['first_name'])
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Ha cancelado el registro del Pago Móvil',
        reply_markup=buttons.menuKeyboard)
    return MAIN


handler = ConversationHandler(
    entry_points=[
        CommandHandler('pagoMovil', get_ref),
        MessageHandler(Filters.regex(
            'Inicio Registro de pago movil'), get_ref),
        MessageHandler(Filters.regex(
            'Cancelar Registro de pago movil'), cancel)
    ],
    states={
        REF: [
            MessageHandler(Filters.text, get_amount)
        ],
        AMOUNT: [
            MessageHandler(Filters.text, get_phone)
        ],
        PHONE: [
            MessageHandler(Filters.text, end_payment)
        ]
    },
    fallbacks=[
        MessageHandler(Filters.regex(
            'Cancelar Registro de pago movil'), cancel)
    ],
    map_to_parent={
        MAIN: MAIN
    }
)
