import logging
from telegram import Update
from telegram.ext import CallbackContext
from src.public.menu.main import commands


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()

command_dict = {
    'Volviendo al Menu': commands.backToMenu,
    '📍   Ver Ubicación': commands.getLocation,
    '📆   Ver Horario': commands.getSchedule,
    '📱 Redes Sociales': commands.getSocialMedia,
    '💲   Ver Tasa de Cambio': commands.getExchange,
    '📓 Contacta al Desarrollador': commands.getDeveloperContact,
    '🔍 Buscar Precios': commands.switchToPrices,
    '💱 Registrar Pago Movil': commands.switchToMobilePayment,
    'Admin': commands.switchToAdminMenu
}


def textHandler(update: Update, context: CallbackContext):
    text = update.message['text']
    if text in command_dict.keys():
        return command_dict[text](update, context)
