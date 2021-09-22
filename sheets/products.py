import utils
import pandas as pd

# Connection To DB
import pyodbc


connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=.;'
                            'Database=MassPanAdmindb;'
                            'Trusted_Connection=yes;')


# Obtaining Google Sheet
sh = utils.getGoogleSpreadsheet(
    utils.PRODUCTS_CREDENTIALS,
    utils.PRODUCTS_SHEET_KEY
)


def load_instances():
    # Obtener todas las instancias de la DB y añadirla a la Sheet
    query = pd.read_sql_query(
        "SELECT [CodInst],[Descrip] FROM [MassPanAdmindb].[dbo].[SAINSTA]", connection
    )
    instance_df = pd.DataFrame(query)

    instances = utils.getOrCreateGoogleWorksheet(
        sh, 'Instances', cols=2, rows=16)
    utils.writeDataframeInSheet(
        instance_df, instances, dont_repeat_on='Descrip')


def load_products():
    # Obtener todos los productos con  sus datos y añadirlo a la Google Sheet
    query = pd.read_sql_query(
        """
        SELECT  prod.CodProd,
            prod.Descrip,
            prod.CodInst,
            prod.Marca,
            prod.Existen,
            prod.Activo,
            usd.Costo,
            usd.Mayor,
            usd.Detal,
            usd.Especial
        FROM [MassPanAdmindb].[dbo].[SAPROD] as prod
        INNER JOIN [MassPanAdmindb].[dbo].[SAPROD_01] AS usd
        ON (prod.CodProd = usd.CodProd)
        """,
        connection
    )
    products_df = pd.DataFrame(query)
    # Filtrando que los productos esten activos
    products_df = products_df.loc[products_df['Activo'] == 1]
    # Filtrando que su precio no sea cero
    products_df = products_df.loc[products_df['Costo'] > 0]
    # Filtrando que los productos no esten en una categoria privada
    products_df = products_df.loc[
        (products_df['CodInst'] != 15) &
        (products_df['CodInst'] != 1025)
    ]
    products = utils.getOrCreateGoogleWorksheet(
        sh, 'Products', cols=10, rows=100)
    utils.writeDataframeInSheet(
        products_df, products, dont_repeat_on='Descrip')


def load_barcodes():
    query = pd.read_sql_query(
        """
    SELECT [CodAlte]
        ,[CodProd]
    FROM [MassPanAdmindb].[dbo].[SACODBAR]
    """,
        connection
    )
    code_df = pd.DataFrame(query)
    code_df
    codes = utils.getOrCreateGoogleWorksheet(sh, 'Barcodes', cols=2)
    utils.writeDataframeInSheet(
        code_df, codes, dont_repeat_on='CodProd')


if __name__ == '__main__':
    # Obtaining Google Sheet
    load_instances()
    load_products()
    load_barcodes()
