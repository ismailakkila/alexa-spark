from __future__ import print_function
import alexaActions
import sparkApi

applicationId = "APP ID"
spark_AccessToken = "SPARK ACCESS TOKEN"
twilio_AccountSid = "TWILIO ACCOUNT SID"
twilio_AuthToken  = "TWILIO AUTH TOKEN"
cellPhoneE164 = "YOUR CELLPHONE NUMBER"
twilioNumber = "YOUR ASSIGNED TWILIO NUMBER"

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] != applicationId):
    	raise ValueError("Invalid Application ID")	
    if event['session']['new']:
       on_session_started({'requestId': event['request']['requestId']}, event['session'])
    event['session']['user']['accessToken'] = spark_AccessToken
    if event['request']['type'] == "LaunchRequest":
    	if 'accessToken' in event['session']['user']:
    		sparkApi.sparkAccessToken = event['session']['user']['accessToken']
    		return on_launch(event['request'], event['session'])
    	else:
    		print ("No Access Token!")
    		session_attributes = {}
    		reprompt_text = None
    		card_title = "Cisco Spark  - Account Setup"
    		speech_output  = "To get started with the Cisco Spark Alexa skill, please login to your Spark account using the Alexa companion app."
    		print ("Alexa Speech Output is: " + speech_output)
    		should_end_session = True
    		return build_response(session_attributes, build_speechlet_response_noAccessToken(card_title, speech_output, reprompt_text, should_end_session))
    elif event['request']['type'] == "IntentRequest":
    	if 'accessToken' in event['session']['user']:
    		sparkApi.sparkAccessToken = event['session']['user']['accessToken']
        	return on_intent(event['request'], event['session'])
        else:
    		print ("No Access Token!")
    		session_attributes = {}
    		reprompt_text = None
    		card_title = "Cisco Spark  - Account Setup"
    		speech_output  = "To get started with the Cisco Spark Alexa skill, please login to your Spark account using the Alexa companion app."
    		print ("Alexa Speech Output is: " + speech_output)
    		should_end_session = True
    		return build_response(session_attributes, build_speechlet_response_noAccessToken(card_title, speech_output, reprompt_text, should_end_session))
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId'] + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] + ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
          
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
	# Dispatch to your skill's intent handlers
    if intent_name == "LatestMessagesIntent":
    	return get_latestMessages_from_session(intent, session)
    elif intent_name == "PostMessageIntent":
    	return post_message_from_session(intent, session)
    elif intent_name == "MessageIntent":
    	return message_from_session(intent, session)
    elif intent_name == "StartJoinMeetingIntent":
    	return startjoinmeeting_from_session(intent, session)
    elif intent_name == "AMAZON.YesIntent":
    	return yes_from_session(intent, session)
    elif intent_name == "AMAZON.NoIntent":
    	return no_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
    	print ("Help Intent Recieved")
    	return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent":
    	return cancel(intent, session)
    else:
    	print ("Invalid intent")
    	if session['attributes']:
    		session_attributes = session['attributes']
    		reprompt_text = None
    		speech_output = "I did not quite understand that. You can try again."
    		print ("Alexa Speech Output is: " + speech_output)
    		should_end_session = False
    	else:
    		session_attributes = {}
    		reprompt_text = None
    		speech_output = "I did not quite understand that. You can try again."
    		print ("Alexa Speech Output is: " + speech_output)
    		should_end_session = False
    	return build_response(session_attributes, build_speechlet_response(intent['name'], speech_output, reprompt_text, should_end_session))
    	#raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
	print ("Intent Request is Welcome")
	session_attributes = {'intentSequence': ['welcome']}
	card_title = "Welcome"
	speech_output = alexaActions.recentActivity()
	reprompt_text = """If you would like me to repeat that, just say: 'recent activity' anytime.
	 				If you would like me to read your recent messages in one of the rooms, just ask: 'what is new in' . followed by the name of the room . For example. what is new in 'Ask Jabber'."
	 				If you would like to post a message to one of the rooms, just say: 'post message to' . followed by the name of the room. For example. post message to Ask Expressway."""
	 				
	speech_output = "Welcome to Cisco Spark. " + speech_output
	print ("Alexa Speech Output is: " + speech_output)
	should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_latestMessages_from_session(intent, session):
	print ("Intent Request is Get Latest Messages")
	print (session)
	print (intent)
	card_title = "What Is New"
	if 'value' in intent['slots']['Room']:
		roomVal = intent['slots']['Room']['value']
		if 'attributes' in session:
			latestIntent = session['attributes']['intentSequence'][-1]
			allowedLatestIntents = ['welcome', 'latestMessages', 'postMessage', 'postMessageRoomDecline', 'postMessageValueConfirm']
			if latestIntent in allowedLatestIntents:
				session['attributes']['intentSequence'].append('latestMessages')
				session_attributes = session['attributes']
				reprompt_text = None
				print ("Room Value in Intent Request is: ", roomVal)
				speech_output = alexaActions.latestMessages(roomVal)
				print ("Alexa Speech Output is: " + speech_output)
				should_end_session = False
			else:
				session_attributes = session['attributes']
				reprompt_text = None
				speech_output = "I did not quite catch that. You can try again."
				print ("Alexa Speech Output is: " + speech_output)
				should_end_session = False
		else:
			session_attributes = {'intentSequence': ['latestMessages']}
			session['attributes'] = session_attributes
			reprompt_text = None
			speech_output = alexaActions.latestMessages(roomVal)
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
	else:
		if 'attributes' in session:
			session_attributes = session['attributes']
		else:
			session_attributes = {}
		reprompt_text = None
		speech_output = "I did not quite catch that. You can try again."
		print ("Alexa Speech Output is: " + speech_output)
		should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def post_message_from_session(intent, session):
	print ("Intent Request is PostMessageIntent")
	print (session)
	print (intent)
	card_title = "Post Message To Room ?"
	if 'value' in intent['slots']['Room']:
		roomVal = intent['slots']['Room']['value']
		if 'attributes' in session:
			latestIntent = session['attributes']['intentSequence'][-1]
			allowedLatestIntents = ['welcome', 'latestMessages', 'postMessage', 'postMessageRoomDecline', 'postMessageValueConfirm']
			if latestIntent in allowedLatestIntents:
				session['attributes']['intentSequence'].append('postMessage')
				reprompt_text = None
				print ("Room Value in Intent Request is: ", roomVal)
				speech_output, roomIdVal = alexaActions.postMessage(roomVal)
				session['attributes']['postMessage'] = {'roomId': roomIdVal}
				session_attributes = session['attributes']
				print ("Alexa Speech Output is: " + speech_output)
				should_end_session = False
			else:
				session_attributes = session['attributes']
				reprompt_text = None
				speech_output = "I did not quite understand that. Please try again."
				print ("Alexa Speech Output is: " + speech_output)
				should_end_session = False
		else:
			session_attributes = {'intentSequence': ['postMessage']}
			session['attributes'] = session_attributes
			reprompt_text = None
			speech_output, roomIdVal = alexaActions.postMessage(roomVal)
			session['attributes']['postMessage'] = {'roomId': roomIdVal}
			session['attributes'] = session_attributes
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
	else:
		if 'attributes' in session:
			session_attributes = session['attributes']
		else:
			session_attributes = {}
		reprompt_text = None
		speech_output = "I did not quite understand that. Please try again."
		print ("Alexa Speech Output is: " + speech_output)
		should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def message_from_session(intent, session):
	print ("Intent Request is Send Message (Prompt)")
	print (session)
	print (intent)
	card_title = "Send Message ?"
	if 'attributes' in session and 'value' in intent['slots']['Message']:
		latestIntent = session['attributes']['intentSequence'][-1]
		message = intent['slots']['Message']['value']
		if (latestIntent == 'postMessageRoomConfirm' or latestIntent == 'postMessageValueDecline') and session['attributes']['postMessage']['roomId'] != None:
			session['attributes']['intentSequence'].append('postMessageValue')
			session['attributes']['postMessage']['message'] = message
			session_attributes = session['attributes']
			reprompt_text = None
			speech_output = "Here is the message: " + message + ". Shall I go ahead and post it for you?"
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
		else:
			session_attributes = session['attributes']
			reprompt_text = None
			speech_output = "I did not quite catch that. You can try again."
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False		
	else:
		session_attributes = {}
		reprompt_text = None
		speech_output = "I did not quite catch that. You can try again."
		print ("Alexa Speech Output is: " + speech_output)
		should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def startjoinmeeting_from_session(intent, session):
	print ("Intent Request is StartJoinMeetingIntent")
	print (session)
	print (intent)
	card_title = "Start/ Join a Meeting ?"
	if 'value' in intent['slots']['Room']:
		roomVal = intent['slots']['Room']['value']
		if 'attributes' in session:
			latestIntent = session['attributes']['intentSequence'][-1]
			allowedLatestIntents = ['welcome', 'latestMessages', 'postMessage', 'postMessageRoomDecline', 'postMessageValueConfirm', 'startJoinMeeting', 'startJoinMeetingDecline']
			if latestIntent in allowedLatestIntents:
				session['attributes']['intentSequence'].append('startJoinMeeting')
				reprompt_text = None
				print ("Room Value in Intent Request is: ", roomVal)
				speech_output, roomIdVal = alexaActions.startJoinMeeting(roomVal)
				session['attributes']['startJoinMeeting'] = {'roomId': roomIdVal}
				session_attributes = session['attributes']
				print ("Alexa Speech Output is: " + speech_output)
				should_end_session = False
			else:
				session_attributes = session['attributes']
				reprompt_text = None
				speech_output = "I did not quite understand that. Please try again."
				print ("Alexa Speech Output is: " + speech_output)
				should_end_session = False
		else:
			session_attributes = {'intentSequence': ['startJoinMeeting']}
			session['attributes'] = session_attributes
			reprompt_text = None
			speech_output, roomIdVal = alexaActions.startJoinMeeting(roomVal)
			session['attributes']['startJoinMeeting'] = {'roomId': roomIdVal}
			session['attributes'] = session_attributes
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
	else:
		if 'attributes' in session:
			session_attributes = session['attributes']
		else:
			session_attributes = {}
		reprompt_text = None
		speech_output = "I did not quite understand that. Please try again."
		print ("Alexa Speech Output is: " + speech_output)
		should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def yes_from_session(intent, session):
	print ("Intent Request is Yes")
	print (session)
	print (intent)
	card_title = "Yes"
	if 'attributes' in session:
		latestIntent = session['attributes']['intentSequence'][-1]
		if latestIntent == 'postMessageValue' and session['attributes']['postMessage']['roomId'] != None and session['attributes']['postMessage']['message']:
			session['attributes']['intentSequence'].append('postMessageValueConfirm')
			session_attributes = session['attributes']
			postRoomId = session['attributes']['postMessage']['roomId']
			postMessage = session['attributes']['postMessage']['message']
			speech_output = alexaActions.sendMessage(postMessage, postRoomId)
			reprompt_text = None
			print ("Intent Request is Yes to postMessageValueConfirm")
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
		elif latestIntent == 'postMessage' and session['attributes']['postMessage']['roomId'] != None:
			session['attributes']['intentSequence'].append('postMessageRoomConfirm')
			session_attributes = session['attributes']
			reprompt_text = 'To post your message, just say: send message . followed by the message to be posted'
			print ("Intent Request is Yes to postMessageRoomConfirm")
			speech_output = "What would you like to say?"
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
		elif latestIntent == 'startJoinMeeting' and session['attributes']['startJoinMeeting']['roomId'] != None:
			session['attributes']['intentSequence'].append('startJoinMeetingConfirm')
			session_attributes = session['attributes']
			startJoinRoomId = session['attributes']['startJoinMeeting']['roomId']
			speech_output = alexaActions.startJoinMeetingAction(startJoinRoomId)
			reprompt_text = None
			print ("Intent Request is Yes to startJoinMeetingConfirm")
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = True
		else:
			session_attributes = session['attributes']
			reprompt_text = None
			speech_output = "I did not quite understand that. Please try again."
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False		
	else:
		session_attributes = {}
		reprompt_text = None
		speech_output = "I did not quite understand that. Please try again."
		print ("Alexa Speech Output is: " + speech_output)
		should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def no_from_session(intent, session):
	print ("Intent Request is No")
	print (session)
	print (intent)
	card_title = "No"
	if 'attributes' in session:
		latestIntent = session['attributes']['intentSequence'][-1]
		if latestIntent == 'postMessageValue' and session['attributes']['postMessage']['roomId'] != None and session['attributes']['postMessage']['message']:
			session['attributes']['intentSequence'].append('postMessageValueDecline')
			del session['attributes']['postMessage']['message']
			session_attributes = session['attributes']
			reprompt_text = None
			speech_output = "Ok. You can repeat your message again or just say cancel."
			print ("Intent Request is No to postMessage - Message")
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
		elif latestIntent == 'postMessage' and session['attributes']['postMessage']['roomId'] != None:
			session['attributes']['intentSequence'].append('postMessageRoomDecline')
			del session['attributes']['postMessage']
			session_attributes = session['attributes']
			reprompt_text = None
			print ("Intent Request is No to postMessage - Room")
			speech_output = "Ok Cancelled. What would you like to do?"
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
		elif latestIntent == 'startJoinMeeting' and session['attributes']['startJoinMeeting']['roomId'] != None:
			session['attributes']['intentSequence'].append('startJoinMeetingDecline')
			del session['attributes']['startJoinMeeting']
			session_attributes = session['attributes']
			reprompt_text = None
			print ("Intent Request is No to startJoinMeeting - Room")
			speech_output = "Ok Cancelled. What would you like to do?"
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False
		else:
			session_attributes = session['attributes']
			reprompt_text = None
			speech_output = "I did not quite catch that. You can try again."
			print ("Alexa Speech Output is: " + speech_output)
			should_end_session = False		
	else:
		session_attributes = {}
		reprompt_text = None
		speech_output = "I did not quite catch that. You can try again."
		print ("Alexa Speech Output is: " + speech_output)
		should_end_session = False
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
	
def cancel(intent, session):
	print ("Cancel Intent Recieved")
	print (session)
	print (intent)
	card_title = "Request Cancelled"
	reprompt_text = None
	session_attributes = {}
	speech_output = "OK"
	print ("Alexa Speech Output is: " + speech_output)
	should_end_session = True
	return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
	    
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response_noAccessToken(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'LinkAccount',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

