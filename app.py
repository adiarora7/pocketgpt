from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
#from random import choice
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = "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"


#below is og code
app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def chatgpt():
    """get incoming message"""
    inb_msg = request.form['Body'].lower()
    print(inb_msg)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=inb_msg,
        max_tokens=3000,
        temperature=0.7
    )
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    # Add a message
    resp.message(response["choices"][0]["text"])
    print(response["choices"][0]["text"])

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)