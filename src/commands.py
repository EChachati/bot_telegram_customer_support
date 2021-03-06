import logging
import os

from telegram import InlineKeyboardMarkup

import buttons
import constants
import database_mysql as mysql
import database_sql_server as sql_server
from utils import get_barcode, add_to_unknown_messages, formated_product_list

global photo_id
photo_id = 0

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def getBotInfo(update, context):
    mybot = context.bot
    chat_id = update.message.chat_id
    name = update.effective_user["first_name"]
    last_name = update.effective_user["last_name"]
    username = update.effective_user.username

    logger.info(f'El user {username} ({name}) ha iniciado el bot')

    if not mysql.is_active_user(chat_id):
        mysql.insert_user(chat_id=chat_id, username=username, first_name=name, last_name=last_name)
        logger.info(f'El user {username} ({name}) se ha añadido a la Database')
        mysql.add_log_to_db(chat_id, f'El user {username} ({name}) se ha añadido a la Database')

    mysql.add_log_to_db(chat_id, f'El user {username} ({name}) ha iniciado el bot')

    mybot.sendMessage(
        chat_id=chat_id,
        parse_mode="HTML",
        text=constants.START_INFO(name),
        reply_markup=buttons.social_networks
    )
    update.message.reply_text(text="Elige un comando: ", reply_markup=buttons.menuKeyboard)


def getSchedule(update, context):
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido el horario al bot')
    try:
        mysql.add_log_to_db(update.message.chat_id, f'El user {username} ({name}) le ha pedido el horario al bot')
        context.bot.sendMessage(chat_id=update.message.chat_id, text=constants.SCHEDULE, parse_mode="HTML")
    except:
        query = update.callback_query
        query.answer()
        query.edit_message_text(text=constants.SCHEDULE, parse_mode='HTML')


def getLocation(update, context):
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(f'El user {username} ({name}) le ha pedido la ubicacion al bot')

    try:
        mysql.add_log_to_db(update.message.chat_id, f'El user {username} ({name}) le ha pedido la ubicacion al bot')
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
        mysql.add_log_to_db(update.message.chat_id,
                            f'El user {username} ({name}) le ha pedido la tasa de cambio al bot')
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
    mysql.add_log_to_db(update.message.chat_id,
                        f'El user {username} ({name}) le ha solicitado la información del desarrollador')

    mybot.sendMessage(
        chat_id=update.message.chat_id,
        parse_mode="HTML",
        text=constants.DEVELOPER_INFO,
        reply_markup=buttons.developer_social_networks
    )


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
        logger.info(f'El user {username} ({name}) ha enviado un código de barras {code}')
        mysql.add_log_to_db(update.message.chat_id,
                            f'El user {username} ({name})  ha enviado un código de barras {code}')
        photo_id += 1
    else:
        logger.info(f'El user {username} ({name}) ha enviado un código de barras')
        product = sql_server.search_product_by_barcode(code)
        if product == {}:
            bot.sendMessage(chat_id=chat_id, text=f"El producto con el código de barras '{code}' no existe")
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
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text=f"Moviendo al Menu precios",
        reply_markup=buttons.pricesKeyboard
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

    elif text == '🔍 Buscar Precios':
        logger.info(f'El user {username} ({name}) Se mueve al menu de precios')
        switch_to_prices_keyboard(update, context)

    elif text == 'Precios Al Mayor':
        sql_server.get_product_list_major(update, context)
        logger.info(f'El User {username} ({name}) solicito la lista de precios al mayor')
        mysql.add_log_to_db(chat_id=update.message.chat_id,
                            text=f'El User {username} ({name}) solicito la lista de precios al mayor')
    elif text == 'Precios Por Categoria':
        update.message.reply_text(text="Elige una Categoria", reply_markup=buttons.intanceKeyboard)
    elif text == 'Buscar por Mensaje':
        update.message.reply_text("Envianos un mensaje con alguna palabra clave del producto buscado")
    elif text == 'Buscar Por Codigo':
        update.message.reply_text("Envianos una foto nitida del código de barras a analizar")
    elif text == 'Volver Al Menu':
        update.message.reply_text(text="Volviendo al Menu", reply_markup=buttons.menuKeyboard)
    elif text == '📱 Redes Sociales':
        logger.info(f'El user {username} ({name}) quiere conocer las redes sociales')
        update.message.reply_text("Siguenos en nuestras Redes Sociales", reply_markup=buttons.social_networks)
    elif text == '📓 Contacta al Desarrollador':
        getContactoDesarrollador(update, context)
    else:
        products = sql_server.search_products_with(text)

        if text in sql_server.INSTANCES.keys():
            products = sql_server.search_products_by_instance(sql_server.INSTANCES[text])
            product_lists = formated_product_list(products)
            logger.info(f'{username}({name}) Ask price for "{text}" products')
            update.message.reply_text(f"PRODUCTOS CATEGORIA: {text}")
            for product_list in product_lists:
                update.message.reply_text(product_list)
            mysql.add_log_to_db(chat_id=update.message.chat_id,
                                text=f"{username}({name}) Ask price for '{text}' products")

        elif products:
            product_lists = formated_product_list(products)
            logger.info(f"{username}({name}) Ask price for '{text}' products")
            for product_list in product_lists:
                update.message.reply_text(product_list)
            mysql.add_log_to_db(chat_id=update.message.chat_id,
                                text=f"{username}({name}) Ask price for '{text}' products)")
        else:
            update.message.reply_text(f"No hay productos relacionados a '{text}'")
            unexcepted_command = (f'{username}({name}) send "{text}" is not a command')
            logger.info(unexcepted_command)
            add_to_unknown_messages(unexcepted_command)
