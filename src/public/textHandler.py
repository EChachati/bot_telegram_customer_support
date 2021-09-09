import logging
from src.public.commands import *
import src.public.buttons
#import database.sqlserver.database_sql_server as sql_server

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()

base_text_command = {
    '📍   Ver Ubicación': getLocation,
    '📆   Ver Horario': getSchedule,
    '🏦   Ver Tasa de Cambio': getExchange,
    '📓 Contacta al Desarrollador': getContactoDesarrollador,

}


def textHandler(update, context):
    # Declarate vars
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    text = (update.message['text'])

    if text in base_text_command.keys():
        base_text_command[text](update, context)

    elif text == 'Precios Por Categoria':
        update.message.reply_text(
            text="Elige una Categoria", reply_markup=buttons.intanceKeyboard)
    elif text == 'Buscar por Mensaje':
        update.message.reply_text(
            "Envianos un mensaje con alguna palabra clave del producto buscado")

    elif text == 'Buscar Por Codigo':
        update.message.reply_text(
            "Envianos una foto nitida del código de barras a analizar")

    elif text == 'Volver Al Menu':
        update.message.reply_text(
            text="Volviendo al Menu", reply_markup=buttons.menuKeyboard)

    elif text == '🔍 Buscar Precios':
        logger.info(f'El user {username} ({name}) Se mueve al menu de precios')
        switch_to_prices_keyboard(update, context)

    elif text == 'Precios Al Mayor':
        sql_server.get_product_list_major(update, context)
        logger.info(
            f'El User {username} ({name}) solicito la lista de precios al mayor')
        mysql.add_log_to_db(chat_id=update.message.chat_id,
                            text=f'El User {username} ({name}) solicito la lista de precios al mayor')

    elif text == '📱 Redes Sociales':
        logger.info(
            f'El user {username} ({name}) quiere conocer las redes sociales')
        update.message.reply_text(
            "Siguenos en nuestras Redes Sociales", reply_markup=buttons.social_networks)

    else:
        products = sql_server.search_products_with(text)

        if text in sql_server.INSTANCES.keys():
            products = sql_server.search_products_by_instance(
                sql_server.INSTANCES[text])
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
            update.message.reply_text(
                f"No hay productos relacionados a '{text}'")
            unexcepted_command = (
                f'{username}({name}) send "{text}" is not a command')
            logger.info(unexcepted_command)
            add_to_unknown_messages(unexcepted_command)
