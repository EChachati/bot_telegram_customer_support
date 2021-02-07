##########################
## Autor Edkar Chachati ##
##########################

import logging  # Para ver lo que hace el bot

import telebot
import telegram
from telegram.ext import Updater, CommandHandler
from selenium import webdriver
from secret import TOKEN

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,"
)
logger = logging.getLogger()

if __name__ == "__main__":
    # obtener info del bot
    bot = telegram.Bot(token=TOKEN)
    print(bot.getMe())

    # Obtener Tasa del dolar
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    driver.get('https://exchangemonitor.net/dolar-promedio-venezuela')
    promedio_tasa_dolar = driver.find_element_by_tag_name('h2').text
    driver.quit()
    #promedio_tasa_dolar = 'xd'
    # print(promedio_tasa_dolar)


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
             f'\n\n Y recuerda <b>¡¡Mass Sabor con Mass Pan!!</b>'
    )


def getHorario(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido el horario al bot')
    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text="Actualmente nuestro horario es de:\n Lunes A Viernes:\n\n 8 A.M. hasta las 4 P.M.\n\n<b> En horario corrido </b>"
    )


def getUbicacion(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la ubicacion al bot')
    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text="Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente al autolavado, Coro (Venezuela), o <a href='https://www.google.com/maps/dir//11.423235,-69.640745/@11.4251583,-69.6442251,16.27z/data=!4m2!4m1!3e0?hl=es'>Ir por GPS</a> "
    )


def getTasaCambio(update, context):
    mybot = context.bot
    chat_id = update.message.chat_id
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la Tasa de Cambio al bot')
    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=f"La Tasa de cambio que manejamos usualmente es la tasa promedio, actualmente es de:\n {promedio_tasa_dolar}"
    )


def getContactoDesarrollador(update, context):
    mybot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha solicitado la información del desarrollador')


    keyboard = telegram.InlineKeyboardButton('Message the developer', url='telegram.me/echachati')
    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=f"Este Bot esta siendo actualmente desarrollado por Edkar Chachati. Redes sociales:\n\n"
             f"  ▪  Instagram<a href='https://www.instagram.com/echachati/'> @EChachati</a>\n"
             f'  ▪  Twitter <a href="https://twitter.com/EJChati">      @EJChati</a>\n'
             f'  ▪  LinkedIn <a href="https://www.linkedin.com/in/echachati?originalSubdomain=ve">    EChachati</a>\n'
             f'  ▪  Github <a href="https://github.com/EjChati">       EJChati</a>\n'
             f'  ▪  Telegram <a href="https://telegram.me/echachati">  @Echachati</a>\n',
        reply_markup=keyboard
    )


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

updater.start_polling()  # Estar verificando si esta recibiendo mensajes, ponte a vivir y existir
updater.idle()  # terminar bot con ctrl+c
