from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from functions import verify_number, update_list, ask, create_msg_object, trim_messages, set_system

#code for the whole web app is nested within the chatgpt function
app = Flask(__name__)

app.config['SECRET_KEY'] = 'couldbeanythinghere'

greetings = ['hey', 'hello', 'hi', 'hey!', 'hello!', 'hi!', 'hi pocketgpt',
             'hey pocketgpt', 'hello pocketgpt', 'hi pocketgpt!',
             'hey pocketgpt!', 'hello pocketgpt!', 'sup']

@app.route("/sms", methods=['POST'])
def chatgpt():
#UPDATE USER LIST - Fetch the database to see if the 
    data = update_list()
    
#CHECK USER - Verify incoming number. If someone isn't registered then a link to the website, is sent.
    """Get incoming number & verify"""
    inb_num = request.form['From']
    if verify_number(inb_num, data) == False:
        resp = MessagingResponse()
        resp.message("Hi! You're not currently signed up for PocketGPT. You can register at pocket-gpt.com")
        return str(resp)
    
#READ MESSAGE AND CREATE&SEND RESPONSE
    else:
        """get incoming message"""
        inb_msg = request.form['Body'].lower()
        print(inb_msg)
        
        #get chatlog
        messages = session.get('chat_log')
        messages = set_system(messages)
        #create question object
        question = create_msg_object("user", inb_msg)
        #append question object to messages
        messages.append(question)
        #ask for response 
        response = ask(messages)
        #create reply object
        reply = create_msg_object("assistant", response)
        #append reply object to messages
        messages.append(reply)
        #update session variable
        session['chat_log'] = messages
        
        #trim messages if there are over 9 saved messages
        messages = session.get('chat_log')
        session['chat_log'] = trim_messages(messages)
        

        #print(session['chat_log'])
        
        resp = MessagingResponse()
        resp.message(response)
        
        return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
