import cv2
from pyzbar.pyzbar import decode

from database_mysql import get_all_users
from src import constants


def get_barcode(path) -> str:
    _code = 'inlegible'
    img = decode(cv2.imread(path))
    for obj in img:
        _code = f'{obj.data}'
    return _code.replace("b", "").replace("'", "")


def actualization_message(bot):
    users = get_all_users()
    for chat_id in users:
        bot.sendMessage(
            chat_id=chat_id,
            text="¡Hola! ¡¡Este bot ha sido actualizado!! Por favor presiona en /start para obtener los cambios,"
                 " se ha añadido: "
                 "\n - Un Menu de acciones"
                 "\n - Lector de codigos de barras por fotos")


def add_to_unknown_messages(string):
    file = open("unknown_messages_file.txt", "a")
    file.write(f'\n{string}')
    file.close()


def formated_product_list(products, precio: int = 2):
    PRECIOS = ['cost', 'mayor', 'detal', 'especial']
    lists = []
    formated_list = ""
    for p in products:
        if len(formated_list) <= 3800:
            formated_list += f"{p['description']}\n" \
                             f"Bs.{p[PRECIOS[precio]]*1712325.45:,.2f}\n\n" # constants.DOLAR_FLOAT:,.2f}\n\n"
        else:
            lists.append(formated_list)
            formated_list = "" + f"{p['description']}\n" \
                             f"Bs.{p[PRECIOS[precio]] * 1712325.45:,.2f}\n\n"  # constants.DOLAR_FLOAT:,.2f}\n\n"
    lists.append(formated_list)
    return lists
