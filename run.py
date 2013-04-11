from flask import Flask, request, render_template, redirect, url_for
import time
import twilio.twiml

app = Flask(__name__)

sensor_states = {}

@app.route("/debug")
def set_status():
    global sensor_states
    now = int(time.time())
    sensor_states = {u'upstairs-wc':{u'status':u'0', u'updated':now}, u'downstairs-wc':{u'status':u'1', u'updated':now}, u'sidestairs-wc':{u'status':u'0', u'updated':now}}
    return redirect('/')

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
    sensor_time = int(time.time())
    global sensor_states
    sensor_states[sensor_id] = {'status': sensor_val, 'updated': sensor_time}
    return  ""

@app.route("/states", methods=['GET'])
def show_state():
    global sensor_states
    return str(sensor_states)

@app.route("/", methods=['GET'])
def web_state():
    global sensor_states
    now = int(time.time())
    return render_template('index.html', sensors=sensor_states, time=now)

def get_sensor_state_msg(sensor_id):
    global sensor_states
    sensor = sensor_states[sensor_id]
    state = sensor.get('status')

    if state == '0':
        return 'The bathroom is vacant.'
    elif state == '1':
        return 'The bathroom is occupied.'
    else:
        return 'The bathroom is undefined.'

if __name__ == '__main__':
    app.debug = True
    app.run()
