from flask import Flask, request, render_template
from datetime import datetime
#import twilio.twiml

app = Flask(__name__)

sensor_states = {}

sensor_template={u'upstairs-wc':{u'status':u'0', u'updated':u'00:00:00 00-00-0000'}
    u'downstairs-wc':{u'status':u'1', u'updated':u'00:00:00 00-00-0000'}
    u'sidestairs-wc':{u'status':u'0', u'updated':u'00:00:00 00-00-0000'}
}

@app.route("/twilio/voice", methods=['POST'])
def twilio_voice():
    """Respond to incoming Twilio voice phone requests."""
    resp = twilio.twiml.Response()
    resp.say(get_sensor_state_msg('upstairs-wc'))
    return str(resp)

@app.route("/twilio/text", methods=['POST'])
def twilio_text():
    """Respond to incoming Twilio SMS text message requests."""
    resp = twilio.twiml.Response()
    resp.sms(get_sensor_state_msg('upstairs-wc'))
    return str(resp)

@app.route("/update", methods=['POST'])
def update_state():
    """Update state following request from remote sensor."""
    sensor_id = request.form['sensor_id']
    sensor_val = request.form['sensor_val']
    sensor_time = datetime.time(datetime.now())
    global sensor_states
    sensor_states[sensor_id] = sensor_val
    return  ""

@app.route("/states", methods=['GET'])
def show_state():
    global sensor_states
    return str(sensor_states)

@app.route("/", methods=['GET'])
def web_state():
    global sensor_states
    time = datetime.time(datetime.now())
    return render_template('index.html', sensors=sensor_states)

def get_sensor_state_msg(sensor_id):
    global sensor_states
    sensor = sensor_states[sensor_id]
    state = sensor_states.get(sensor_id)

    if state == '0':
        return 'The bathroom is vacant.'
    elif state == '1':
        return 'The bathroom is occupied.'
    else:
        return 'The bathroom is undefined.'

if __name__ == '__main__':
    app.debug = True
    app.run()
