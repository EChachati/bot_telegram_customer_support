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
        d[row[0]] = row[1]
    return d


def get_prices_from_barcode(barcode: str):
    cursor.execute(f"SELECT [Costo],[Mayor],[Detal],[Especial] "
                   f"FROM [MassPanAdmindb].[dbo].[SAPROD_01] "
                   f"WHERE [CodProd] = '{barcode}'")
    for row in cursor:
        return row


def search_product_by_barcode(barcode: str):
    product = {}
    cursor.execute(f"SELECT [CodProd], [Descrip], [CodInst], [Marca], [Existen] "
                   f"FROM [MassPanAdmindb].[dbo].[SAPROD] "
                   f"WHERE [CodProd] = '{barcode}'")
    for row in cursor:
        prices = get_prices_from_barcode(barcode)
        product = {
            'code': row[0],
            'description': row[1],
            'instance': row[2],
            'brand': row[3],
            'exist': float(row[4]),
            'cost': float(prices[0]),
            'mayor': float(prices[1]),
            'detal': float(prices[2]),
            'special': float(prices[3])
        }

    return product


def search_products_with(text: str):
    products = []
    cursor.execute(f"SELECT [CodProd], [Descrip], [CodInst], [Marca], [Existen] "
                   f"FROM [MassPanAdmindb].[dbo].[SAPROD] "
                   f"WHERE [Descrip] LIKE '%{text}%'")
    for row in cursor:
        products.append({
            'code': row[0],
            'description': row[1],
            'instance': row[2],
            'brand': row[3],
            'exist': float(row[4])
        })
    return products


# Constants
INSTANCES = __get_instances()

if __name__ == "__main__":
    print(search_product_by_barcode('7597827000106'))
    print(search_product_by_barcode('1111111111111'))
