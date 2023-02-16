import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
#from random import choice
from dotenv import load_dotenv
import openai
from verification import verify_number, update_list

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

#start_sequence = "\nPocketGPT:"
#restart_sequence = "\n\nPerson:"
session_prompt = "You are PocketGPT, you have the same functionalities as ChatGPT.\n\nPerson: Hi\nPocketGPT: Hi there! How can I help you?\n\nPerson:"


#below is og code
app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def chatgpt():
    
    """Update list"""
    data= update_list()
    """Check incoming number"""
    
    inb_num = request.form['From']
    #if verify_number(inb_num, data) == False:
        #resp = MessagingResponse()
       # resp.message("Hi! You're not currently signed up for PocketGPT. To access PocketGPT, sign up for free at https://pocket-gpt.com/free-signup/")
        #return str(resp)
    
    if int(inb_num)==17787107707:
        """get incoming message"""
        inb_msg = request.form['Body'].lower()
        print(inb_msg)
        temp = 0.7
        if inb_msg == 'hey':
            temp = 0.1
        #prompt_text = inb_msg
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=inb_msg,
            max_tokens=3000,
            temperature=temp,
        )
        """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
        resp = MessagingResponse()
    # Add a message
        resp.message(response["choices"][0]["text"])
        print(response["choices"][0]["text"])

        return str(resp)
    
    elif verify_number(inb_num, data) == True:
        resp = MessagingResponse()
        resp.message("Hi, we appreciate you using PocketGPT! We appreciate your patience as we refine the model. PocketGPT will be up soon.")
        return str(resp)
    
    else:
        resp = MessagingResponse()
        resp.message("Hi! You're not currently signed up for PocketGPT. To be notified about the release of PocketGPT, sign up at https://pocket-gpt.com/free-signup/")
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)