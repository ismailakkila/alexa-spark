from flask import Flask, request

app = Flask(__name__)

@app.route('/twilio/<sipUri>', methods=['GET', 'POST'])
def twilio(sipUri):
	twilioSipXml = '''<?xml version="1.0" encoding="UTF-8"?><Response><Say voice="woman">Joining Your Spark Room</Say><Dial><Sip>sip:''' + sipUri + ";transport=tcp</Sip></Dial></Response>"
	return twilioSipXml

if __name__ == '__main__':
	app.run(host='0.0.0.0')