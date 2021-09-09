import pyodbc

connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=.;'
                            'Database=MassPanAdmindb;'
                            'Trusted_Connection=yes;')

cursor = connection.cursor()


# SAINSTA for instance
def __get_instances():
    d = {}
    cursor.execute("SELECT [CodInst],[Descrip] FROM [MassPanAdmindb].[dbo].[SAINSTA]")
    for row in cursor:
        d[row[1]] = row[0]
    return d


def search_product_by_barcode(barcode: str):
    product = {}
    cursor.execute(
        f"SELECT prod.CodProd, prod.Descrip, prod.CodInst, prod.Marca, prod.Existen, "
        f"usd.Costo, usd.Mayor, usd.Detal, usd.Especial "
        f"FROM [MassPanAdmindb].[dbo].[SAPROD] as prod INNER JOIN [MassPanAdmindb].[dbo].[SAPROD_01] AS usd "
        f"ON (prod.CodProd = usd.CodProd) WHERE prod.[CodProd] = '{barcode}'")
    for row in cursor:
        product = {'code': row[0],
                   'description': row[1],
                   'instance': row[2],
                   'brand': row[3],
                   'exist': float(row[4]),
                   'cost': float(row[5]),
                   'mayor': float(row[6]),
                   'detal': float(row[7]),
                   'special': float(row[8]),
                   }
    return product


def search_products_with(text: str):
    products = []
    cursor.execute(f"SELECT prod.CodProd, prod.Descrip, prod.CodInst, prod.Marca, prod.Existen, "
                   f"usd.Costo, usd.Mayor, usd.Detal, usd.Especial "
                   f"FROM [MassPanAdmindb].[dbo].[SAPROD] as prod "
                   f"INNER JOIN [MassPanAdmindb].[dbo].[SAPROD_01] AS usd "
                   f"ON (prod.CodProd = usd.CodProd) "
                   f"WHERE prod.[Descrip] LIKE '%{text}%'")
    for row in cursor:
        products.append(
            {'code': row[0],
             'description': row[1],
             'instance': row[2],
             'brand': row[3],
             'exist': float(row[4]),
             'cost': float(row[5]),
             'mayor': float(row[6]),
             'detal': float(row[7]),
             'special': float(row[8]),
             })
    return products


def get_product_list_major(update, context):  # TOFIX
    products = []
    cursor.execute(
        f"SELECT prod.CodProd, prod.Descrip, prod.CodInst, prod.Marca, prod.Existen, usd.Costo, usd.Mayor, usd.Detal, usd.Especial FROM [MassPanAdmindb].[dbo].[SAPROD] as prod INNER JOIN [MassPanAdmindb].[dbo].[SAPROD_01] AS usd ON (prod.CodProd = usd.CodProd) WHERE prod.Marca = 'EL TUNAL' OR prod.Marca = 'MANTORO' OR prod.Marca = 'CASCADA' OR prod.Marca = 'ST MORITZ' OR  prod.Marca = 'MASS PAN'")
    for row in cursor:
        products.append(
            {'code': row[0],
             'description': row[1],
             'instance': row[2],
             'brand': row[3],
             'exist': float(row[4]),
             'cost': float(row[5]),
             'mayor': float(row[6]),
             'detal': float(row[7]),
             'special': float(row[8]),
             })
    from src.utils import formated_product_list
    formated_list = formated_product_list(products, precio=1)
    for product_list in formated_list:
        update.message.reply_text(product_list)
    return formated_product_list(products)


def search_products_by_instance(instance: int):
    products = []
    cursor.execute(f"SELECT prod.CodProd, prod.Descrip, prod.CodInst, prod.Marca, prod.Existen, usd.Costo, usd.Mayor, usd.Detal, usd.Especial FROM [MassPanAdmindb].[dbo].[SAPROD] as prod INNER JOIN [MassPanAdmindb].[dbo].[SAPROD_01] AS usd ON (prod.CodProd = usd.CodProd) WHERE prod.CodInst = {instance}")
    for row in cursor:
        products.append(
            {'code': row[0],
             'description': row[1],
             'instance': row[2],
             'brand': row[3],
             'exist': float(row[4]),
             'cost': float(row[5]),
             'mayor': float(row[6]),
             'detal': float(row[7]),
             'special': float(row[8]),
             })
    return products


# Constants
INSTANCES = __get_instances()

"""*************************************** NOT USED ***************************************"""
"""*************************************** NOT USED ***************************************"""
"""*************************************** NOT USED ***************************************"""
"""*************************************** NOT USED ***************************************"""


def get_prices_from_barcode(barcode: str):
    cursor.execute(f"SELECT [Costo],[Mayor],[Detal],[Especial] "
                   f"FROM [MassPanAdmindb].[dbo].[SAPROD_01] "
                   f"WHERE [CodProd] = '{barcode}'")
    for row in cursor:
        return [float(row[0]), float(row[1]), float(row[2]), float(row[3])]
    return []


"""*************************************** NOT USED ***************************************"""
"""*************************************** NOT USED ***************************************"""
"""*************************************** NOT USED ***************************************"""
"""*************************************** NOT USED ***************************************"""
