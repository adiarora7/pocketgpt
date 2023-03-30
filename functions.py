import os
from dotenv import load_dotenv
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

session_prompt =  {"role":"system", "content": "You are a helpful assistant."}
initial_user = {"role": "user", "content": "Who won the world series in 2020?"}
initial_ai = {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."}

def set_system(messages):
    if messages is None:
        messages=[session_prompt, initial_user, initial_ai]
    return messages

def ask(messages):
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )
    
    reply = completion['choices'][0]['message']['content']
    print(str(reply))
    return str(reply)

def create_msg_object(role, content):
    #creating a msg object to be appended to messages
    msg_object = {"role": role, "content": content}
    return msg_object


def trim_messages(messages):
    #if there are >9 messages then remove oldest interaction
    if len(messages) >= 9:
        messages = messages[:1]+messages[3:]
        
    return messages

def update_list():
# Set the path to the service account key file
    KEY_PATH = '/etc/secrets/pocketgpt-81dc23062dda.json'
#KEY_PATH = '/Users/adiarora/Downloads/pocketgpt-81dc23062dda.json'
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

#add a 1 to the beginning of each number
    values = [[str('1') + item for item in inner_list] for inner_list in values]
    #outputs values from Column 1 in google sheets
    values = [[int(item) for item in inner_list] for inner_list in values[1:]]
#print(values)
    return values

""" Checks if input is in list of numbers that are signed up"""
def verify_number(incoming_number, values):
    if int(incoming_number) in [integer for inner_list in values for integer in inner_list]:
        return True
    else:
        return False
