import telegram
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from datetime import datetime


# Methods
def get_dolar_value():
    # Obtener Tasa del dolar
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    driver.get('https://exchangemonitor.net/dolar-promedio-venezuela')
    promedio_tasa_dolar = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, 'h2'))).text
    driver.quit()
    return promedio_tasa_dolar


# String Constants
DOLAR = get_dolar_value()
EXCHANGE_VALUE = f"La Tasa de cambio que manejamos usualmente es la tasa promedio, actualmente es de:\n {DOLAR}"


def START_INFO(name: str = ""):
    return (
        f'¡Hola {name}! Soy un bot encargado de ayudarte con tus compras en la Panaderia Mass Pan, sin embargo, aun '
        f'me encuentro en desarrollo, puedes escribirle a nuestro equipo @MassPan o al número de telefono +58 412 773 6899 '
        f'para resolver tu dudas\n\n'
        f'Puedes clickear en estos /comandos :\n'
        f'  📍   /ubicacion\n'
        f'  📆   /horario\n'
        f'  🏦   /tasaCambio\n'
        f'\n Y recuerda <b>¡¡Mass Sabor con Mass Pan!!</b>'
        f'\n\n Contactanos con las siguentes apps'
        f'\n  👇👇👇👇👇👇👇👇👇👇👇👇')


SCHEDULE = (
    "Actualmente nuestro horario es de:\n Lunes A Viernes:\n\n 8 A.M. hasta las 4 P.M.\n\n<b> En horario corrido </b>")

LOCATION = "Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente" \
           " al autolavado, Coro (Venezuela)"

DEVELOPER_INFO = "Este Bot esta siendo actualmente desarrollado por Edkar Chachati. Redes sociales:\n\n"

gps_location = telegram.Location(latitude=11.423235, longitude=-69.640745)
