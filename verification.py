import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set the path to the service account key file
KEY_PATH = '/Users/adiarora/Downloads/pocketgpt-81dc23062dda.json'

# Set the ID of the spreadsheet you want to access
SPREADSHEET_ID = '1_YyNmPJyLpFaNhQTkuXlD98EcK5pRZqmC6fgYGroBcI'

# Authenticate using the service account
creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

# Build the Sheets API client
service = build('sheets', 'v4', credentials=creds)

# range of cells to retrieve (in this case, all cells in Column 1)
range_name = 'Sheet1!A:A'

# Make the API request to retrieve the cell values
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
values = result.get('values', [])

# Print the values
#if not values:
#    print('No data found.')
#else:
#    print('User Phone Numbers:')
    #outputs values from Column 1 in google sheets
values = [[int(item) for item in inner_list] for inner_list in values[1:]]

def verify_number(incoming_number):
    if int(incoming_number) in values:
        return True
    else:
        return False