from src.states import *
import logging
import pandas as pd
from telegram import (
    Update,
    ReplyKeyboardRemove
)
from telegram.ext import CallbackContext

from src.public.product import (
    buttons,
    utils
)
from src.public.menu.main import buttons as menu

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def price_type(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    logger.info(
        f'El user {username} ({name}) Va a registró el tipo de precio (Mayor, Menor)')
    try:
        if context.user_data['price_type']:
            pass
    except KeyError:
        context.user_data['price_type'] = update.message.text
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text='¿De que manera deseas realizar la busqueda? Tenemos las siguentes opciones',
        reply_markup=buttons.searchTypeKeyboard
    )
    return PRICE_TYPE


def search_type(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    text = update.message.text
    if text == 'Buscar por Categoria':
        logger.info(
            f'El user {username} ({name}) Eligió Busqueda por categoria')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Categorias de productos disponibles',
            reply_markup=buttons.categoryMenu()
        )
        return SEARCH_CAT

    elif text == 'Buscar por Codigo de Barras':
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Envianos una imagen con el código de barras del producto que desees o envianos un mensaje con el código para buscarlo c:',
            reply_markup=ReplyKeyboardRemove()
        )
        logger.info(
            f'El user {username} ({name}) Eligió Busqueda por codigo de barras')
        return SEARCH_CODE

    elif text == 'Buscar por Nombre del Producto':
        logger.info(
            f'El user {username} ({name}) Eligió Busqueda por nombre del producto')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Envianos un mensaje con el producto que deseas buscar, te enviaremos todos los que tengan en su nombre el contenido de tu mensaje  c:',
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH_NAME

    else:
        logger.info(f'El user {username} ({name}) Eligió ir al menu')
        return cancel(update, context)


def categoryHandler(update: Update, context: CallbackContext) -> int:
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    text_inst = update.message.text
    if text_inst == 'Volver al Menu de Precios':
        logger.info(
            f'El user {username} ({name}) Eligió ir al menu de precios')
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text='Volviendo al menu de Precios',
            reply_markup=buttons.searchTypeKeyboard
        )
        return PRICE_TYPE
    elif text_inst == 'Volver al Menu Principal':
        return cancel(update, context)
    else:
        logger.info(
            f'El user {username} ({name}) Solicitó precios de la instanvia {text_inst}')
        df = utils.getProductDataFrame()
        instance_df = utils.getInstanceDataFrame()
        inst = int(
            instance_df.loc[instance_df['Descrip'] == text_inst]['CodInst']
        )

        if context.user_data['price_type'] == 'Precio al por Mayor':
            df = df.loc[df['CodInst'] == inst][['Descrip', 'Mayor']]
            text = f'{text_inst} (Precio al Mayor)\n'
        else:
            df = df.loc[df['CodInst'] == inst][['Descrip', 'Detal']]
            text = f'{text_inst} (Precio Regular)\n'

        for i in df.values.tolist():
            text += f'{i[0]} ➡️ {i[1]}$ ({i[1] * 4_100_000} Bs)\n'

        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=text,
            reply_markup=buttons.categoryMenu()
        )
        return SEARCH_CAT


def searchByName(update: Update, context: CallbackContext):
    text = update.message.text.upper()
    df = utils.getProductDataFrame()
    df = df.loc[df['Descrip'].str.contains(
        text)][['Descrip', 'Mayor', 'Detal']]
    info = f'Productos con {text} en su nombre:\n'
    if context.user_data['price_type'] == 'Precio al por Mayor':
        for e in df.to_dict(orient='records'):
            info += f'{e["Descrip"]} ➡️ {e["Mayor"]}$ ({e["Mayor"] * 4_100_000} Bs)\n'
    else:
        for e in df.to_dict(orient='records'):
            info += f'{e["Descrip"]} ➡️ {e["Detal"]}$ ({e["Detal"] * 4_100_000} Bs)\n'

    if len(info) > 4096:
        for x in range(0, len(info), 4096):
            context.bot.send_message(
                chat_id=update.message.chat.id,
                text=info[x:x+4096],
                reply_markup=buttons.categoryMenu()
            )
    else:
        context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=info,
            reply_markup=buttons.categoryMenu()
        )

    return price_type(update, context)


def cancel(update: Update, context: CallbackContext) -> int:
    logger.info("User %s back to the main menu.",
                update.effective_user['first_name'])
    context.bot.sendMessage(
        chat_id=update.message.chat_id,
        text='Ha vuelto al menu principal',
        reply_markup=menu.menuKeyboard)
    return MAIN
