from __future__ import print_function
import re
import sparkApi
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def recentActivity():
	roomsListDict = sparkApi.get('rooms')
	if roomsListDict != 'Error':
		roomsListParsed = []
		lastActivityList = []
		roomsString = ''
		for roomItem in roomsListDict['items']:
			roomsListParsed.append({'Name': roomItem['title'], 'ID':  roomItem['id'], 'Last Activity': roomItem['lastActivity'] })
			lastActivityList.append(roomItem['lastActivity'])
			roomsString = roomsString + roomItem['title'] + '\n'
		print ("This is the List of Rooms For the User:\n" + roomsString)
		print ("Determining the Rooms With the Most Recent Activity (Up to 5)")
		lastActivityListParsed = []
		for iteration in range(0,5):
			mostRecentActivity = max(lastActivityList)
			mostRecentActivityIndex = lastActivityList.index(mostRecentActivity)
			lastActivityListParsed.append(mostRecentActivity)
			lastActivityList.pop(mostRecentActivityIndex)
		#print (lastActivityListParsed)
		#print (roomsListParsed)
		roomListLastActivity = []
		roomsStringLastActivity = ''
		roomIndex = 0
		speech_output = "You have recent activity in the following last five spark rooms: . "
		for lastActivity in lastActivityListParsed:
			for room in roomsListParsed:
				if room['Last Activity'] == lastActivity:
					roomListLastActivity.append(room)
					speech_output = speech_output + " , " + roomListLastActivity[roomIndex]['Name']
					roomsStringLastActivity = roomsStringLastActivity + roomListLastActivity[roomIndex]['Name'] + '\n'
					roomIndex = roomIndex + 1
		print ("This is the List of Rooms With the Most Recent Activity (Up to 5):\n" + roomsStringLastActivity)
		print ("Alexa Speech Output is: " + speech_output)
	else:
		speech_output = "There was an issue connecting to Cisco Spark. Please try again in a few minutes."
	return speech_output

def latestMessages(roomVal):
	roomsListDict = sparkApi.get('rooms')
	if roomsListDict != 'Error':
		roomsListParsed = []
		roomsMatchList = []
		roomsString = ''
		for room in roomsListDict['items']:
			roomsListParsed.append({'Name': room['title'], 'ID':  room['id']})
			roomsMatchList.append(room['title'])
			roomsString = roomsString + room['title'] + '\n'
		print ("This is the List of Rooms For the User:\n" + roomsString)
		print ("Finding Closest Match...")
		roomMatchTuple = process.extractOne(roomVal, roomsMatchList)
		roomMatch = roomMatchTuple[0]
		roomMatchScore = roomMatchTuple[1]
		print ("Closest Match for Room Title is: ", roomMatch)
		print ("Room Match Score: ", roomMatchScore)
		if roomMatchScore >= 85:
			for room in roomsListParsed:
				if room['Name'] == roomMatch:
					roomId = room['ID']
			print ("Room ID is: ", roomId)
			whatsNewResponse = sparkApi.get('messages', {'roomId': roomId, 'max': '3'})
			if whatsNewResponse != 'Error':
	 			if len(whatsNewResponse['items']) > 0:
					whatsNewList = []
					for messageInfoDict in whatsNewResponse['items']:
						whatsNewDict = {}
						if 'text' in messageInfoDict and 'personId' in messageInfoDict and messageInfoDict['personId'] != "":
							messageText = messageInfoDict['text']
							personId = messageInfoDict['personId']
							displayNameDict = sparkApi.get('people', {'personId': personId})
							if 'displayName' in displayNameDict and displayNameDict['displayName'] !="":
								displayName = re.sub(r'\([^)]*\)', '', displayNameDict['displayName'])
							else:
								displayName = 'Unknown'
							whatsNewDict = {'Name': displayName, 'Message': messageText}
							whatsNewList.append(whatsNewDict)
						else:
							continue
					#print ("Whats New List: ", whatsNewList)
					print ("Constructing Alexa Speech Output...")
					speechOutput = "Your most recent messages in spark room " + ": " + roomMatch
					for item in range(len(whatsNewList) - 1, -1, -1):
						if item == len(whatsNewList) - 1:
							speechOutput = speechOutput + ". Message from " + whatsNewList[item]['Name'] + " .. " + whatsNewList[item]['Message']
						if item == len(whatsNewList) - 2:
							speechOutput = speechOutput + ". Followed by message from " + whatsNewList[item]['Name'] + " .. " + whatsNewList[item]['Message']
						if item == len(whatsNewList) - 3:
							speechOutput = speechOutput + ". And finally, from " + whatsNewList[item]['Name'] + " .. " + whatsNewList[item]['Message']
				else:
					print ("There Are No Messages In This Room")
					speechOutput = "Unfortuantely, there are no messages in spark room: " + roomMatch	
			else:
				print ("There was an issue connecting to Cisco Spark. Please try again in a few minutes.")
				speechOutput = "There was an issue connecting to Cisco Spark. Please try again in a few minutes."
		else:
			print ("Room Match < Required Score! Inappropriate Match")
			speechOutput = "I could not find an appropriate match for the room you mentioned. Please try again."
	else:
		print ("There was an issue connecting to Cisco Spark. Please try again in a few minutes.")
		speechOutput = "There was an issue connecting to Cisco Spark. Please try again in a few minutes."
	return speechOutput
	
def postMessage(roomVal):
	roomsListDict = sparkApi.get('rooms')
	if roomsListDict != 'Error':
		roomsListParsed = []
		roomsMatchList = []
		roomsString = ''
		for room in roomsListDict['items']:
			roomsListParsed.append({'Name': room['title'], 'ID':  room['id']})
			roomsMatchList.append(room['title'])
			roomsString = roomsString + room['title'] + '\n'
		print ("This is the List of Rooms For the User:\n" + roomsString)
		print ("Finding Closest Match...")
		roomMatchTuple = process.extractOne(roomVal, roomsMatchList)
		roomMatch = roomMatchTuple[0]
		roomMatchScore = roomMatchTuple[1]
		print ("Closest Match for Room Title is: ", roomMatch)
		print ("Room Match Score: ", roomMatchScore)
		if roomMatchScore >= 85:
			for room in roomsListParsed:
				if room['Name'] == roomMatch:
					roomIdValue = room['ID']
			print ("Room ID is: ", roomIdValue)
			speechOutput = "Post Message to Spark Room: " + roomMatch + " . Shall I proceed?"
		else:
			print ("Room Does Not Exist For User")
			speechOutput = "I'm not sure what your spark room is. You can try again."
			roomIdValue = None
	else:
		speech_output = "There is a problem connecting to the Cisco Spark. Please try again in a few minutes."
		roomIdValue = None
	return speechOutput, roomIdValue

def sendMessage(messageVal, postRoomIdVal):
	postResponse = sparkApi.post('messages', {'roomId': postRoomIdVal, 'text': messageVal})
	if postResponse != 'Error':
		speechOutput = "Posting your message"
		return speechOutput
	else:
		speechOutput = "There is a problem connecting to Cisco Spark. Please try again in a few minutes."
		return speechOutput
		