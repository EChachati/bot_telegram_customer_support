import gspread as gs
import pandas as pd
import sheets.utils

# https://www.youtube.com/watch?v=T1vqS1NL89E

GOOGLE_CREDENTIALS = 'sheets\credentials.json'
ACCOUNT_STATE_SHEET_KEY = '1qsssy55XNV-j49jHiA2QlCvDwUrCc0IKsYR6HBfSx6A'


def run():
    spreadsheet = utils.getGoogleSpreadsheet(
        GOOGLE_CREDENTIALS, ACCOUNT_STATE_SHEET_KEY)
    df = pd.DataFrame(spreadsheet.sheet1.get_all_records())
    df = utils.cleanFloatsInColumn(df, 'Monto')
    df = utils.cleanDateInColumn(df, 'Fecha')
    incomePagoMovilSheet = utils.getOrCreateGoogleWorksheet(
        spreadsheet,
        name='Ingreso Pago Movil'
    )
    incomePagoMovil = df.loc[(df['Descripción'] == 'Banesco Pago Movil') & (
        df['Monto'] > 0)][['Fecha', 'Referencia', 'Descripción', 'Monto']]
    utils.writeDataframeInSheet(
        incomePagoMovil,
        incomePagoMovilSheet,
        dont_repeat_on='Referencia')


if __name__ == '__main__':
    run()
