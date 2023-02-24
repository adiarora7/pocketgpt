from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from functions import verify_number, update_list, ask, append_interaction_to_chat_log, trim_chat_log

#code for the whole web app is nested within the chatgpt function
app = Flask(__name__)

app.config['SECRET_KEY'] = 'hgtgniser5443'

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
        resp.message("Hi! You're not currently signed up for PocketGPT. Sign up to be notified of the release at pocket-gpt.com/coming-soon")
        return str(resp)
    
#READ MESSAGE AND CREATE&SEND RESPONSE
    else:
        """get incoming message"""
        inb_msg = request.form['Body'].lower()
        print(inb_msg)
        
        """if inb_msg is greeting"""
        if inb_msg in greetings:
            resp = MessagingResponse()
            reply = "Hey there! How can I help you?"
            resp.message(reply)
            print (resp)
            return str(resp)
        
        else:
            """otherwise generate reply"""
            #get chatlog
            chat_log = session.get('chat_log')
            #ask for response 
            response = ask(inb_msg, chat_log)
            #set chatlog to chatlog + question + response
            session['chat_log'] = append_interaction_to_chat_log(inb_msg,
                                    response,
                                    chat_log)
            
            #print chatlog
            chat_log = session.get('chat_log')
            session['chat_log'] = trim_chat_log(chat_log)
            

            #print(session['chat_log'])
            
            resp = MessagingResponse()
            resp.message(response)
            
            return str(resp)

if __name__ == "__main__":
    app.run(debug=True)