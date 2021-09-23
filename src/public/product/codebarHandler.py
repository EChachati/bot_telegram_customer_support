import logging
import os
import cv2
from pyzbar.pyzbar import decode
from sheets import utils
from src.public.product.utils import *
from src.public.product import buttons
from src.states import *
from telegram.ext import CallbackContext
from telegram import Update


global photo_id
photo_id = 0

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


def get_barcode(path) -> str:
    code = 'ilegible'
    img = decode(cv2.imread(path))
    for obj in img:
        code = f'{obj.data}'
    return code.replace("b", "").replace("'", "")


def searchProductByBarcode(code):
    codes = getBarcodeDataFrame()
    prod_df = getProductDataFrame()

    try:
        codProd = list(
            set(
                codes.loc[codes['CodAlte'] == str(code)]['CodProd']
            )
        )[0]
    except IndexError:
        return {}

    prod = prod_df.loc[prod_df['CodProd'] == codProd].head(
        1)[['Descrip', 'Mayor', 'Detal']].to_dict(orient='records')[0]
    return prod


def codebarImageHandler(update: Update, context: CallbackContext) -> int:
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
        bot.sendMessage(
            chat_id=chat_id,
            text=f"El Código de barras es {code}. Intente de nuevo enviando otra imagen o escribiendo el código"
        )
        logger.info(
            f'El user {username} ({name}) ha enviado un código de barras {code}')
        photo_id += 1
        return SEARCH_CODE
    else:
        product = searchProductByBarcode(code)

        if product == {}:
            bot.sendMessage(
                chat_id=chat_id,
                text=f"El producto con el código de barras '{code}' no existe",
                reply_markup=buttons.searchTypeKeyboard
            )
            photo_id += 1
            logger.info(
                f'El user {username} ({name}) ha enviado un código de barras no registrado {code}')

        else:

            if context.user_data['price_type'] == 'Precio al por Mayor':
                price = product['Mayor']
            else:
                price = product['Detal']

            # Delete the file
            os.remove(f'{photo_id}.jpg')
            bot.sendMessage(
                chat_id=chat_id,
                text=f"{product['Descrip']} ➡️ {price}$ ({price * 4_100_000} Bs)",
                reply_markup=buttons.searchTypeKeyboard
            )
            logger.info(
                f'El user {username} ({name}) ha recibido el precio del producto {product["Descrip"]} {product["Detal"]}$')
        return PRICE_TYPE


def codebarTextHandler(update: Update, context: CallbackContext) -> int:

    bot = context.bot
    username = update.effective_user.username
    name = update.effective_user["first_name"]
    code = update.message.text
    chat_id = update.message.chat_id

    product = searchProductByBarcode(code)

    if context.user_data['price_type'] == 'Precio al por Mayor':
        price = product['Mayor']
    else:
        price = product['Detal']

    if product == {}:
        bot.sendMessage(
            chat_id=chat_id,
            text=f"El producto con el código de barras '{code}' no existe",
            reply_markup=buttons.searchTypeKeyboard
        )
        logger.info(
            f'El user {username} ({name}) ha enviado un código de barras no registrado {code}'
        )

    else:
        bot.sendMessage(
            chat_id=chat_id,
            text=f"{product['Descrip']} ➡️ {price}$ ({price * 4_100_000} Bs)",
            reply_markup=buttons.searchTypeKeyboard
        )
        logger.info(
            f'El user {username} ({name}) ha recibido el precio del producto {product["Descrip"]} {price}$'
        )
    return PRICE_TYPE
