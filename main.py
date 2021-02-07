########################
# Autor Edkar Chachati #
#   Twitter @EJChati   #
########################

import logging  # Para ver lo que hace el bot

import telegram
import constants
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler
from secret import TOKEN

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
        text=f'¡Hola {name}! Soy un bot encargado de ayudarte con tus compras en la Panaderia Mass Pan, sin embargo aun '
             f'me encuentro en desarrollo, puedes escribirle a nuestro equipo @MassPan o al número de telefono +58 412 773 6899 '
             f'para resolver tu dudas\n\n'
             f'Puedes clickear en estos comandos:\n'
             f'  📍   /ubicacion\n'
             f'  📆   /horario\n'
             f'  🏦   /tasaCambio\n\n'
             f'Puedes seguirnos en nuestras redes sociales:\n'
             f'  ▪  Instagram<a href="https://www.instagram.com/masspanve/"> @MassPanVe</a>\n'
             f'  ▪  Facebook <a href="https://www.facebook.com/masspanve/"> Panadería Mass Pan</a>\n'
             f'  ▪  WhatsApp <a href="https://www.whatsapp.com/catalog/584127736899/?app_absent=0"> +584127736899</a>'
             f'\n\n Y recuerda <b>¡¡Mass Sabor con Mass Pan!!</b>',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text=' 📍   Ver Ubicación ', callback_data="ubicacion")],  # TODO Fix
        ])
    )


def getHorario(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido el horario al bot')
    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.HORARIO
    )


def getUbicacion(update, context):
    mybot = context.bot
    print(update)
    # chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la ubicacion al bot')

    update.message.reply_text(parse_mode="HTML", text=constants.UBICACION)

    # mybot.sendMessage(
    #    chat_id=chat_id,
    #    parse_mode="HTML",
    #    text="Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente al autolavado, Coro (Venezuela), o <a href='https://www.google.com/maps/dir//11.423235,-69.640745/@11.4251583,-69.6442251,16.27z/data=!4m2!4m1!3e0?hl=es'>Ir por GPS</a> "
    # )


def getTasaCambio(update, context):
    mybot = context.bot
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la Tasa de Cambio al bot')
    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=constants.get_tasa_cambio(promedio_tasa_dolar)
    )


def getContactoDesarrollador(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha solicitado la información del desarrollador')

    button_contacta_al_desarrollador = InlineKeyboardButton(text='Contactar al desarrollador', url="telegram.me/echachati")

    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.DEVELOPER_INFO,
        reply_markup=InlineKeyboardMarkup([
            [button_contacta_al_desarrollador],
        ])
    )


if __name__ == "__main__":
    # obtener info del bot
    bot = telegram.Bot(token=TOKEN)
    print(bot.getMe())

    promedio_tasa_dolar = constants.get_dolar_value()

    # updater se conecta y recibe los mensajes
    # noinspection PyUnboundLocalVariable
    updater = Updater(bot.token, use_context=True)

    # crear despachador
    dispatcher = updater.dispatcher

    # crear comando
    dispatcher.add_handler(CommandHandler("start", getBotInfo))
    dispatcher.add_handler(CommandHandler("horario", getHorario))
    dispatcher.add_handler(CommandHandler("ubicacion", getUbicacion))
    dispatcher.add_handler(CommandHandler("tasaCambio", getTasaCambio))
    dispatcher.add_handler(CommandHandler("contact", getContactoDesarrollador))

    # Empezar a ejecutar el bot
    updater.start_polling()  # Estar verificando si esta recibiendo mensajes, ponte a vivir y existir
    updater.idle()  # terminar bot con ctrl+c
