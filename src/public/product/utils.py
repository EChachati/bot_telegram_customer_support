from sheets import utils
import pandas as pd


def getInstanceDataFrame():
    sh = utils.getGoogleSpreadsheet(
        utils.PRODUCTS_CREDENTIALS,
        utils.PRODUCTS_SHEET_KEY
    )
    sheet = utils.getOrCreateGoogleWorksheet(sh, 'Instances')
    df = pd.DataFrame(sheet.get_all_records())
    df = df.loc[
        (df['CodInst'] != 1025) &  # Factor
        (df['CodInst'] != 15) &    # Insumos Internos
        (df['CodInst'] != 24)      # Combos
    ]
    return df


def getProductDataFrame():
    sh = utils.getGoogleSpreadsheet(
        utils.PRODUCTS_CREDENTIALS,
        utils.PRODUCTS_SHEET_KEY
    )
    sheet = utils.getOrCreateGoogleWorksheet(sh, 'Products')
    return pd.DataFrame(
        sheet.get_all_records(
            value_render_option='UNFORMATTED_VALUE',
            numericise_ignore=['all']
        )
    )


def getBarcodeDataFrame():
    sh = utils.getGoogleSpreadsheet(
        utils.PRODUCTS_CREDENTIALS,
        utils.PRODUCTS_SHEET_KEY
    )
    sheet = utils.getOrCreateGoogleWorksheet(sh, 'Barcodes')
    return pd.DataFrame(
        sheet.get_all_records(numericise_ignore=['all'])
    )
