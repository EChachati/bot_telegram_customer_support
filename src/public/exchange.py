from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


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


#__DOLAR = get_dolar_value()
#DOLAR_STR = __DOLAR[0]
#DOLAR_FLOAT = __DOLAR[1]

#EXCHANGE_VALUE = f"La Tasa de cambio que manejamos usualmente es la tasa promedio, actualmente es de:\n {DOLAR_STR}"
