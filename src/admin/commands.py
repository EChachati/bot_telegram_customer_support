from telegram.ext.dispatcher import Dispatcher
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler
from src.admin.users import ADMIN_USERS
from sheets import utils
import pandas as pd
from src.states import *
import logging
from src.admin.users import *
from src.admin.menu import buttons as adminButtons


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def get_all_pm_status(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    if chat_id in ADMIN_USERS:
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
            text=text
        )


def add_commands(dispatcher: Dispatcher) -> Dispatcher:
    d = dispatcher
    d.add_handler(CommandHandler('PMStatus', get_all_pm_status))
    # d.add_handler(CommandHandler('admin', switchToAdminMenu))
    return d
