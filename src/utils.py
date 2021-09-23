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


def cleanFloat(x) -> float:
    x = str(x)
    if ',' in str(x) and not '.' in str(x):  # 321,21
        x = str(x).replace(',', '.')
    elif '.' in str(x) and ',' in str(x):  # 321.210,12
        x = str(x).replace('.', '').replace(',', '.')

    return float(x)
