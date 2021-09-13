import telegram


def START_INFO(name: str = ""):
    return (
        f'¡Hola {name}! Soy un bot encargado de ayudarte con tus compras en la Panaderia Mass Pan, sin embargo, aun '
        f'me encuentro en desarrollo, puedes escribirle a nuestro equipo @MassPan o al número de telefono +58 412 773 6899 '
        f'para resolver tu dudas\n\n'
        f'Puedes moverte usando nuestro menu, o escribir algún producto en el que estes interesado\n'
        f'\n Y recuerda <b>¡¡Mass Sabor con Mass Pan!!</b>'
        f'\n\n Contactanos con las siguentes apps'
        f'\n  👇👇👇👇👇👇👇👇👇👇👇👇')


LOCATION = "Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente al autolavado, Coro (Venezuela)"

SCHEDULE = (
    "Actualmente nuestro horario es de:\n Lunes A Viernes:\n\n 8 A.M. hasta las 4 P.M.\n\n<b> En horario corrido </b>"
)

GPS_LOCATION = telegram.Location(latitude=11.423235, longitude=-69.640745)

DEVELOPER_INFO = "Este Bot esta siendo actualmente desarrollado por Edkar Chachati. Redes sociales:\n\n"
