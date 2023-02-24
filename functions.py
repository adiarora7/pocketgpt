import os
from dotenv import load_dotenv
import openai
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()
openai.api_key = os.getenv("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")

start_sequence = "\nAI:"
restart_sequence = "\nMe:"
session_prompt =  "Me: Hey\nAI: Hey there! How can I help you?"

def ask(question, chat_log=None):
    prompt_text = f'{session_prompt}{chat_log}{restart_sequence} {question}{start_sequence}'
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt_text,
      temperature=0.66,
      max_tokens=3000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.3,
      stop=["\nMe:"],
    )
    reply = response['choices'][0]['text']
    print(str(reply))
    return str(reply)

def append_interaction_to_chat_log(question, answer, chat_log=None):
    #creating a string literal by concatenating '\nMe: + question + '\nAI: + response
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'


def trim_chat_log(chat_log=None):
    if chat_log is None:
        return ''
    #split string into list of messages
    messages = chat_log.split('\n')
    #if length is greater than or equal to 6(3 interactions), get rid of the oldest interaction
    if len(messages) >= 6:
        messages = messages[1:]
        chatlog = "\n".join(messages)
        print(chatlog)
        return chatlog
    return chat_log

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