import gspread as gs
import pandas as pd

# https://www.youtube.com/watch?v=T1vqS1NL89E

GOOGLE_CREDENTIALS = 'sheets\credentials.json'
ACCOUNT_STATE_SHEET_KEY = '1qsssy55XNV-j49jHiA2QlCvDwUrCc0IKsYR6HBfSx6A'


def getGoogleSpreadsheet(google_credentials, document_key):
    credentials = gs.service_account(filename=google_credentials)
    return credentials.open_by_key(document_key)


def cleanFloatsInColumn(df: pd.DataFrame, column: str) -> pd.DataFrame:
    new_df = df.copy()
    new_df[column] = new_df[column].astype(str).apply(
        lambda x: x.replace('.', '').replace(',', '.')).astype(float)
    return new_df


def cleanDateInColumn(df: pd.DataFrame, column: str) -> pd.DataFrame:
    from datetime import datetime
    new_df = df.copy()
    new_df[column].astype(str).apply(
        lambda x: datetime.strptime(x, '%d/%m/%Y')
    )
    return new_df


def getOrCreateGoogleWorksheet(spreadsheet, name: str, rows="100", cols="4"):
    try:
        sheet = spreadsheet.worksheet(name)
    except:
        sheet = spreadsheet.add_worksheet(
            title=name, rows=rows, cols=cols
        )
    return sheet


def writeDataframeInSheet(df, sheet, dont_repeat_on=None):
    columns = df.columns.values.tolist()
    rows = df.values.tolist()
    sheet_df = pd.DataFrame(sheet.get_all_records())

    if dont_repeat_on:
        assert type(dont_repeat_on) == str
        index = columns.index(dont_repeat_on)
        if sheet_df.empty:
            values = set()
        else:
            values = set(sheet_df[dont_repeat_on])

    if sheet_df.empty or sheet_df.columns.values.tolist() != columns:
        sheet.append_row(columns)

    for row in rows:
        if dont_repeat_on:
            if row[index] not in values:
                sheet.append_row(row)
            else:
                pass
        else:
            sheet.append_row(row)
