from flask import Flask
import twilio.twiml

app = Flask(__name__)

@app.route("/twilio/voice", methods=['POST'])
def twilio_voice():
    """Respond to incoming Twilio voice phone requests."""
    resp = twilio.twiml.Response()
    resp.say("Hello Monkey")
    return str(resp)

@app.route("/twilio/text", methods=['POST'])
def twilio_text():
    """Respond to incoming Twilio SMS text message requests."""
    resp = twilio.twiml.Response()
    resp.sms("Hello Monkey")
    return str(resp)
