from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import pandas as pd
from sheets import utils
from src.public.product.utils import *

priceTypeKeyboard = ReplyKeyboardMarkup([
    ['Precio Regular'],
    ['Precio al por Mayor']
])

searchTypeKeyboard = ReplyKeyboardMarkup([
    ['Buscar por Categoria'],
    ['Buscar por Codigo de Barras'],
    ['Buscar por Nombre del Producto'],
    ['Volver al Menu Principal']
])


def categoryMenu():
    df = getInstanceDataFrame()
    menu = []
    for e in df['Descrip'].tolist():
        menu.append([e])
    menu.append(['Volver al Menu de Precios'])
    menu.append(['Volver al Menu Principal'])
    return ReplyKeyboardMarkup(menu)
