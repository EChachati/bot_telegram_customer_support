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
                 "\n - Escribe un mensaje con algún código que quieras buscar"
                 "\n - Puedes moverte por nuestros menus para buscar precios al por mayor y por categoria"
                 "\n - Lector de codigos de barras por fotos"
                 "\n\nCualquier error que encuentres por favor notificalo para que sea arreglado")


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
                             f"Bs.{p[PRECIOS[precio]] * constants.DOLAR_FLOAT:,.2f}  ${p[PRECIOS[precio]]}\n\n"
        else:
            lists.append(formated_list)
            formated_list = "" + f"{p['description']}\n" \
                                 f"Bs.{p[PRECIOS[precio]] * constants.DOLAR_FLOAT:,.2f}  ${p[PRECIOS[precio]]}\n\n"
    lists.append(formated_list)
    return lists
