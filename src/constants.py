import telegram
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# Methods
def get_dolar_value():
    # Obtener Tasa del dolar
    #    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://exchangemonitor.net/dolar-promedio-venezuela')
    promedio_tasa_dolar: str = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.TAG_NAME, 'h2'))).text
    driver.quit()
    promedio_tasa_dolar_float = promedio_tasa_dolar.replace(" ", "") \
        .replace("BS/USD", "") \
        .replace("VES/USD", "") \
        .replace(".", "_") \
        .replace(",", ".")
    return [promedio_tasa_dolar, float(promedio_tasa_dolar_float)]


# String Constants
__DOLAR = get_dolar_value()
DOLAR_STR = __DOLAR[0]
DOLAR_FLOAT = __DOLAR[1]

EXCHANGE_VALUE = f"La Tasa de cambio que manejamos usualmente es la tasa promedio, actualmente es de:\n {DOLAR_STR}"


def START_INFO(name: str = ""):
    return (
        f'¡Hola {name}! Soy un bot encargado de ayudarte con tus compras en la Panaderia Mass Pan, sin embargo, aun '
        f'me encuentro en desarrollo, puedes escribirle a nuestro equipo @MassPan o al número de telefono +58 412 773 6899 '
        f'para resolver tu dudas\n\n'
        f'Puedes moverte usando nuestro menu, o escribir algún producto en el que estes interesado\n'
        f'\n Y recuerda <b>¡¡Mass Sabor con Mass Pan!!</b>'
        f'\n\n Contactanos con las siguentes apps'
        f'\n  👇👇👇👇👇👇👇👇👇👇👇👇')


SCHEDULE = (
    "Actualmente nuestro horario es de:\n Lunes A Viernes:\n\n 8 A.M. hasta las 4 P.M.\n\n<b> En horario corrido </b>")

LOCATION = "Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente" \
           " al autolavado, Coro (Venezuela)"

DEVELOPER_INFO = "Este Bot esta siendo actualmente desarrollado por Edkar Chachati. Redes sociales:\n\n"

gps_location = telegram.Location(latitude=11.423235, longitude=-69.640745)
