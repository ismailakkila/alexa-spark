# alexa-spark

All of the pieces for an Amazon Echo (Alexa) <-> Cisco Spark integration.

# Usage

* Recent Activity: Echo will inform you of the last 5 rooms with recent activity.
  
  "Alexa, Open Spark"

  Once the skill is 'triggered' with "Open Spark", you can say the following anytime during the session to retieve you recent activity:
  
  "Any Recent Activity"
  
  "Any Recent Updates"
  
  "Can You Repeat That"
  

* Recent Messages: Echo will inform you of the most recent chat messages (up to 3) within a Spark Room.
  
  "Alexa, Ask Spark What is New in {Spark Room}"
  
  "Alexa, Ask Spark What is New in Room {Spark Room}"

  Once the skill is 'triggered' with "Open Spark", you can say the following anytime during the session to retieve you recent room messages:
 
  "What is New in {Spark Room}"
 
  "What is New in Room {Spark Room}"
  

* Post Message (Experimental): Echo will post a message to one of your Spark Rooms.
 
  "Alexa, Ask Spark to Post Message to {Spark Room}"
 
  "Alexa, Ask Spark to Post Message to Room {Spark Room}"

  Alexa will ask you to confirm your room. Once confirmed, you can say "Send Message: Your Message". Confirm again to have your            message sent.


  Once the skill is 'triggered' with "Open Spark", you can say the following anytime during the session to post your room message:
 
  "Post Message to {Spark Room}"
 
  "Post Message to Room {Spark Room}"
  

* Optional: Start or Join a Meeting (Requires Twilio for now, Tropo is coming): Echo will enable a call-back to your phone and bridge the call to your Spark room (via SIP URI)  to either start or join an existing meeting in that room.
  
  "Alexa, Ask Spark to Start a Meeting in {Spark Room}"
  
  "Alexa, Ask Spark to Start a Meeting in Room {Spark Room}"
  
  "Alexa, Ask Spark to Join a Meeting in {Spark Room}"
  
  "Alexa, Ask Spark to Join a Meeting in Room {Spark Room}"

   Alexa will ask you to confirm your room. Once confirmed, the call-back will be initiated.
   

  Once the skill is 'triggered' with "Open Spark", you can say the following anytime during the session to start or join your meeting:
  
  "Start a Meeting in {Spark Room}"
  
  "Start a Meeting in Room {Spark Room}"
  
  "Join a Meeting in {Spark Room}"
  
  "Join a Meeting in Room {Spark Room}"
  

# How it works

1. When you say the command to Alexa, it triggers the Alexa skill with the invocation name Spark.
2. The Alexa skill calls a web service running on AWS Lambda, passing it the Spark room name.
3. Lambda then fires an API request (GET/ POST) to Spark with the appropriate parameters required to carry out the command.
4. Based on the response, Lambda returns the required speech output to the Alexa skill for possible further actions.

Included here are the Alexa Skill configuration, the Lambda AWS service that catches the Alexa requests, and an example "Room Slot" configuration.

To set it up, you need to do the following:

# Create a Spark Account
1. Please go to https://developer.ciscospark.com and create your account.
2. Make note of your access token as it will be used to connect to the Spark API platform.

# Create a Twilio Account (Optional)
1. Please go to twilio.com to create your account. You will need to buy a "Twilio Telephone Number" to enable calling out from the platform.
2. You will also need to define a URL path that will return the Twilio XML (TwiML). The AWS Lambda service will make the following HTTP GET Request: http://path/to/url/twilio/1234@domain.com where the variable defined is "http://path/to/url/twilio". It will append the SIP URI of the Spark room that will be bridged to the call on your cellphone. I have provided a simple python webhook server in the 'twilioXML' folder. I will leave this up to you to decide on how you would like to deploy it.
3. Make note of the following paramters: Account SID, Auth Token, Your E164 Telephone Number (+12321234567), Twilio Telephone Number and TWiml XML URL Path. 

# Create the Alexa Skill that will send events to AWS Lambda
1. Create a new Skill in the Alexa Skills control panel on Amazon. You need a developer account to do this.
2. Name can be whatever you want. "Invocation" is what you say (I used "Spark").
3. Put a dummy value in the Endpoint. We'll come back to this.
4. Click Next, taking you to Interaction Model. Copy this repo's "alexa-skill/intent_schema.json" into the "Intent Schema" field, and "alexa-skill/utterances.txt" into "Sample Utterances".
5. Still in Interaction Model, create a Custom Slot Type ("Add Slot Type"). Add a new type for ROOM. For accuracy, I would recommend that you export all your room titles from Spark. There is a script.py in the folder that would allow you to retrieve your list of rooms. Replace sparkAcccessToken with your actual token:
  
  python /path/to/script.py sparkAccessToken

7. Copy/paste these values. I have provided an example in the alexa-skill folder.
6. Click back to "Skill Information" and make note of the "Application ID". You'll need this for Lambda.

# Configure the AWS Lambda service that will trigger your API calls
1. Create an AWS Lambda account if you don't have one already. It's free!
2. In the Lambda console, look to the upper right. Make sure "N. Virginia" is selected, because not every zone supports Alexa yet.
3. Create a new Lambda function. Skip the blueprint. 
4. Pick any name you want, and choose runtime Python.
5. Go into this repo's "lambda" directory, modify main.py to edit the following variables that you made a note of in the previous steps:
  
    applicationId = "APP ID"
    
    spark_AccessToken = "SPARK ACCESS TOKEN"
    
    twilio_AccountSid = "TWILIO ACCOUNT SID"
    
    twilio_AuthToken  = "TWILIO AUTH TOKEN"
    
    cellPhoneE164 = "YOUR CELLPHONE NUMBER"
    
    twilioNumber = "YOUR ASSIGNED TWILIO NUMBER"
    
    twilioXmlPath = "TwiML URL PATH"
    
6. Zip up all the files. Make sure you don't capture the folder, just the files.
7. Choose to upload the zip file in lambda.
8. The handler should be: "main.lambda_handler". Create a new role of type Basic Execution Role. Pick smallest possible memory and so on. Increase Timeout Value to 5 mins.
9. Click Next to proceed. Once created, click "Event Sources".
10. Add a source.  Choose "Alexa Skills Kit".

# Connect Alexa Skill to AWS Lambda
1. In the Lambda console, copy the long "ARN" string in the upper right.  
2. Go back into the Alexa Skill console, open your skill, click "Skill Information", choose Lambda ARN and paste that ARN string in.
3. Now you're ready to put it all together. Try "Alexa, Open Spark" to test.

Good Luck!
