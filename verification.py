import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use your Google credentials to authorize access to your Google Sheet
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/credentials.json', scope)
client = gspread.authorize(creds)

# open the Google Sheet containing the numbers
sheet = client.open("Your Sheet Name").sheet1

# get all the numbers from the first column
numbers = sheet.col_values(1)

# convert the numbers from string to integer
numbers = [int(x) for x in numbers]
