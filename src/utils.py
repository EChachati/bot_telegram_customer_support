import cv2
from pyzbar.pyzbar import decode

from database_mysql import get_all_users


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


def format_float(value: float):
    #value = round(value, 2)

    print(f'{value:,.2f}')


if __name__ == "__main__":
    format_float(2041085.208)
