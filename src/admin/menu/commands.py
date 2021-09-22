import logging
import datetime
from sheets import utils
import pandas as pd
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from src.admin.users import *
from src.states import *
from src.admin.menu import buttons
from src.public.menu.main import buttons as publicButtons

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def menu(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    print('someting')
    if is_admin(chat_id):
        logger.info(
            f'El Admin {username} ({name}) Accedio al menu de admin')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Menu Admin',
            reply_markup=buttons.menuKeyboard
        )
        return ADMIN
    else:
        logger.info(
            f'El user {username} ({name}) intento acceder al menu de admin, Acceso Denegado')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Acceso Denegado',
            reply_markup=publicButtons.menuKeyboard
        )
        return MAIN


def getPM(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]

    if is_admin(chat_id):
        logger.info(
            f'El Admin {username} ({name}) solicito los ultimos pago movil')
        sh = utils.getGoogleSpreadsheet(
            utils.GOOGLE_CREDENTIALS,
            utils.ACCOUNT_STATE_SHEET_KEY
        )
        sheet = utils.getOrCreateGoogleWorksheet(sh, 'Ingreso Pago Movil')
        df = pd.DataFrame(sheet.get_all_records())[
            ['Fecha', 'Referencia', 'Monto', 'Estado']]
        text = str(df.tail(20))

        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            reply_markup=buttons.menuKeyboard
        )
        return ADMIN
    else:
        logger.info(
            f'El user {username} ({name}) intento acceder al menu de admin, Acceso Denegado')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Acceso Denegado',
            reply_markup=publicButtons.menuKeyboard
        )
        return MAIN


def getConfirmedPM(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]

    if is_admin(chat_id):
        logger.info(
            f'El Admin {username} ({name}) solicito los ultimos pago moviles confirmados')
        sh = utils.getGoogleSpreadsheet(
            utils.GOOGLE_CREDENTIALS,
            utils.ACCOUNT_STATE_SHEET_KEY
        )
        sheet = utils.getOrCreateGoogleWorksheet(sh, 'Ingreso Pago Movil')
        df = pd.DataFrame(sheet.get_all_records())
        df = df[['Fecha', 'Referencia', 'Monto', 'USD', 'Estado']]
        df = df.loc[df['Estado'] == 'Verificado']
        df = df[['Fecha', 'Referencia', 'Monto', 'USD']]
        text = str(df.tail(20))
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            reply_markup=buttons.menuKeyboard
        )
        return ADMIN
    else:
        logger.info(
            f'El user {username} ({name}) intento acceder a los ultimos pago movil confirmados, Acceso Denegado')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Acceso Denegado',
            reply_markup=publicButtons.menuKeyboard
        )
        return MAIN


def getUnconfirmedPM(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]

    if is_admin(chat_id):
        logger.info(
            f'El Admin {username} ({name}) solicito los ultimos pago moviles no confirmados')
        sh = utils.getGoogleSpreadsheet(
            utils.GOOGLE_CREDENTIALS,
            utils.ACCOUNT_STATE_SHEET_KEY
        )
        sheet = utils.getOrCreateGoogleWorksheet(sh, 'Ingreso Pago Movil')
        df = pd.DataFrame(sheet.get_all_records())[
            ['Fecha', 'Referencia', 'Monto', 'USD', 'Estado']]
        df = df.loc[df['Estado'] == 'No Verificado']
        df = df[['Fecha', 'Referencia', 'Monto', 'USD']]
        text = str(df.tail(20))
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            reply_markup=buttons.menuKeyboard
        )
        return ADMIN
    else:
        logger.info(
            f'El user {username} ({name}) intento acceder a los ultimos pago movil no confirmados, Acceso Denegado')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Acceso Denegado',
            reply_markup=publicButtons.menuKeyboard
        )
        return MAIN


def recordsNotFounds(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]

    if is_admin(chat_id):
        logger.info(
            f'El Admin {username} ({name}) solicito los ultimos registros no confirmados')
        sh = utils.getGoogleSpreadsheet(
            utils.GOOGLE_CREDENTIALS,
            utils.ACCOUNT_STATE_SHEET_KEY
        )

        sheet = utils.getOrCreateGoogleWorksheet(sh, 'TLG Pago Movil')
        pm_sheet = sh.worksheet('Ingreso Pago Movil')
        df = pd.DataFrame(sheet.get_all_records())
        df = df.loc[df['Estado'] == 'No Verificado']
        df = df[['first_name', 'last_name', 'Telefono', 'Referencia', 'Monto']]
        text = str(df.tail(20))
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            reply_markup=buttons.menuKeyboard
        )
        return ADMIN
    else:
        logger.info(
            f'El user {username} ({name}) intento acceder a los ultimos registros no encontrados, Acceso Denegado')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Acceso Denegado',
            reply_markup=publicButtons.menuKeyboard
        )
        return MAIN


def totalPM(update: Update, context: CallbackContext) -> int:
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]

    if is_admin(chat_id):
        logger.info(
            f'El Admin {username} ({name}) solicito los totales en pago movil')
        sh = utils.getGoogleSpreadsheet(
            utils.GOOGLE_CREDENTIALS,
            utils.ACCOUNT_STATE_SHEET_KEY
        )
        pm_sheet = utils.getOrCreateGoogleWorksheet(sh, 'Ingreso Pago Movil')
        pm_df = pd.DataFrame(pm_sheet.get_all_records())
        usd_sheet = utils.getOrCreateGoogleWorksheet(sh, 'Historico USD-VES')
        usd_df = pd.DataFrame(usd_sheet.get_all_records())
        usd_df.set_index('Fecha')
        usd_dic = usd_df.set_index('Fecha').to_dict(orient='index')
        empty_pm = pm_df.loc[pm_df['USD'] == '']
        for i, e in empty_pm.iterrows():
            date = e['Fecha']
            usd = float(usd_dic[date]['Valor'].replace('.', ''))
            ves = float(e['Monto'].replace('.', '').replace(',', '.'))
            empty_pm.at[i, 'USD'] = round(ves / usd, 2)
            empty_pm.at[i, 'Monto'] = round(ves, 2)
        empty_pm['Fecha'] = pd.to_datetime(
            empty_pm['Fecha'], format='%d/%m/%Y')
        empty_pm.loc[(empty_pm['Fecha'].dt.month == 6)]
        # Actual Month
        # datetime.datetime.today().month
        text = f"""Monto Total del mes:
        USD: {round(sum(empty_pm['USD'].tolist()),2)} $
        VES: {round(sum(empty_pm['Monto'].tolist()),2)} Bs"""
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            reply_markup=buttons.menuKeyboard
        )
        return ADMIN
    else:
        logger.info(
            f'El user {username} ({name}) intento acceder a los los totales en pago movil, Acceso Denegado')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Acceso Denegado',
            reply_markup=publicButtons.menuKeyboard
        )
        return MAIN


def backToMenu(update: Update, context: CallbackContext):
    return MAIN
