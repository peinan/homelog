import gspread
from oauth2client.service_account import ServiceAccountCredentials


def auth():
    scopes = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scopes)
    gclient = gspread.authorize(credentials)
    gs = gclient.open('homelog')

    return gs


def append_row(gs, values: list):
    value_input_option = 'USER_ENTERED'

    print(f'values: {values}')

    r = gs.values_append(
        'main_sheet!A:F',
        {'valueInputOption': value_input_option},
        {'values': [values]}
    )

    return r

