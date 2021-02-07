from selenium import webdriver


# Methods
def get_dolar_value():
    # Obtener Tasa del dolar
    driver = webdriver.Chrome("C:\Program Files (x86)\chromedriver.exe")
    driver.get('https://exchangemonitor.net/dolar-promedio-venezuela')
    promedio_tasa_dolar = driver.find_element_by_tag_name('h2').text
    driver.quit()
    return promedio_tasa_dolar


def get_tasa_cambio(
        promedio_tasa_dolar: int): return f"La Tasa de cambio que manejamos usualmente es la tasa promedio, " \
                                          f"actualmente es de:\n {promedio_tasa_dolar}"


# String Constants
START_INFO = (
    f'¡Hola! Soy un bot encargado de ayudarte con tus compras en la Panaderia Mass Pan, sin embargo aun '
    f'me encuentro en desarrollo, puedes escribirle a nuestro equipo @MassPan o al número de telefono +58 412 773 6899 '
    f'para resolver tu dudas\n\n'
    f'Puedes clickear en estos comandos:\n'
    f'  📍   /ubicacion\n'
    f'  📆   /horario\n'
    f'  🏦   /tasaCambio\n\n'
    f'Puedes seguirnos en nuestras redes sociales:\n'
    f'  ▪  Instagram<a href="https://www.instagram.com/masspanve/"> @MassPanVe</a>\n'
    f'  ▪  Facebook <a href="https://www.facebook.com/masspanve/"> Panadería Mass Pan</a>\n'
    f'  ▪  WhatsApp <a href="https://www.whatsapp.com/catalog/584127736899/?app_absent=0"> +584127736899</a>'
    f'\n\n Y recuerda <b>¡¡Mass Sabor con Mass Pan!!</b>')

HORARIO = (
    "Actualmente nuestro horario es de:\n Lunes A Viernes:\n\n 8 A.M. hasta las 4 P.M.\n\n<b> En horario corrido </b>")

UBICACION = "Nos encontramos en Urb. Independencia, 1 Era Etapa, calle 23 (calle siguente a la Urb. Tomas Marzal) frente" \
            " al autolavado, Coro (Venezuela), o <a href='https://www.google.com/maps/dir//11.423235,-69.640745" \
            "/@11.4251583,-69.6442251,16.27z/data=!4m2!4m1!3e0?hl=es'>Ir por GPS</a> "

DEVELOPER_INFO = (f"Este Bot esta siendo actualmente desarrollado por Edkar Chachati. Redes sociales:\n\n"
                  f"  ▪  Instagram<a href='https://www.instagram.com/echachati/'> @EChachati</a>\n"
                  f'  ▪  Twitter <a href="https://twitter.com/EJChati">      @EJChati</a>\n'
                  f'  ▪  LinkedIn <a href="https://www.linkedin.com/in/echachati?originalSubdomain=ve">    EChachati</a>\n'
                  f'  ▪  Github <a href="https://github.com/EjChati">       EJChati</a>\n'
                  f'  ▪  Telegram <a href="https://telegram.me/echachati">  @Echachati</a>\n')
