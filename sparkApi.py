#!/usr/bin/python
import sys, urllib, urllib2, json

sparkDeveloperUrl = 'https://api.ciscospark.com/v1'
sparkAccessToken = None

def getRequest(urlRequest, sparkAccessToken):
	try:
		req = urllib2.Request(urlRequest)
		req.add_header('Accept','application/json')
		req.add_header('Content-Type','application/json; charset=UTF-8')
		req.add_header('Authorization','Bearer ' + sparkAccessToken)
		response = urllib2.urlopen(req)
		result = response.read()
		resultDict = json.loads(result)
		return resultDict
	except urllib2.HTTPError, err:
		return "Error"
	except urllib2.URLError, err:
		return "Error"
	
def postRequest(urlRequest, sparkAccessToken, postBody):
	try:
		req = urllib2.Request(urlRequest)
		req.add_header('Accept','application/json')
		req.add_header('Content-Type','application/json; charset=UTF-8')
		req.add_header('Authorization','Bearer ' + sparkAccessToken)
		json_postBody = json.dumps(postBody)
		response = urllib2.urlopen(req, json_postBody)
		result = response.read()
		return result
	except urllib2.HTTPError, err:
		return "Error"
	except urllib2.URLError, err:
		return "Error"

def get(getMethod, getMethodData=None):
 	if sparkAccessToken != None:
		if getMethod == 'people':
			if getMethodData == None:
				url = sparkDeveloperUrl + '/' + getMethod + '/' + 'me'
				peopleResponseDict = getRequest(url, sparkAccessToken)
				return peopleResponseDict
			if isinstance(getMethodData, dict) and 'personId' in getMethodData:
				url = sparkDeveloperUrl + '/' + getMethod + '/' + getMethodData['personId']
				peopleResponseDict = getRequest(url, sparkAccessToken)
				return peopleResponseDict
			elif isinstance(getMethodData, dict):
				getMethodDataEncode = urllib.urlencode(getMethodData)
				url = sparkDeveloperUrl + '/' + getMethod + '/' + '?' + getMethodDataEncode
				peopleResponseDict = getRequest(url, sparkAccessToken)
				return peopleResponseDict
			return 'Unsupported Get Request Query!'
		if getMethod == 'messages':
			if isinstance(getMethodData, dict) and 'messageId' in getMethodData:
				url = sparkDeveloperUrl + '/' + getMethod + '/' + getMethodData['messageId']
				messageResponseDict = getRequest(url, sparkAccessToken)
				return messageResponseDict
			elif isinstance(getMethodData, dict):
				getMethodDataEncode = urllib.urlencode(getMethodData)
				url = sparkDeveloperUrl + '/' + getMethod + '/' + '?' + getMethodDataEncode
				messageResponseDict = getRequest(url, sparkAccessToken)
				return messageResponseDict
			return 'Unsupported Get Request Query!'
		elif getMethod == 'rooms':
			if getMethodData == None:
				url = sparkDeveloperUrl + '/' + getMethod + '/'
				roomsResponseDict = getRequest(url, sparkAccessToken)
				return roomsResponseDict
			if isinstance(getMethodData, dict) and 'roomId' in getMethodData:
				url = sparkDeveloperUrl + '/' + getMethod + '/' + getMethodData['roomId']
				roomsResponseDict = getRequest(url, sparkAccessToken)
				return roomsResponseDict
			elif isinstance(getMethodData, dict):
				getMethodDataEncode = urllib.urlencode(getMethodData)
				url = sparkDeveloperUrl + '/' + getMethod + '/' + '?' + getMethodDataEncode
				roomsResponseDict = getRequest(url, sparkAccessToken)
				return roomsResponseDict
			return 'Unsupported Get Request Query!'	
		else:
			return 'Unsupported Get Request!'
	else:
		return 'Access token Is Required'
		
def post(postMethod, postMethodData):
	if sparkAccessToken != None:
		if postMethod == 'messages':
			if isinstance(postMethodData, dict) and {'roomId', 'text'}.issubset(postMethodData):
				url = sparkDeveloperUrl + '/' + postMethod + '/'
				postMessageResponseDict = postRequest(url, sparkAccessToken, postMethodData)
				return postMessageResponseDict
			if isinstance(postMethodData, dict) and {'toPersonId', 'text'}.issubset(postMethodData):
				url = sparkDeveloperUrl + '/' + postMethod + '/'
				postMessageResponseDict = postRequest(url, sparkAccessToken, postMethodData)
				return postMessageResponseDict
			if isinstance(postMethodData, dict) and {'toPersonEmail', 'text'}.issubset(postMethodData):
				url = sparkDeveloperUrl + '/' + postMethod + '/'
				postMessageResponseDict = postRequest(url, sparkAccessToken, postMethodData)
				return postMessageResponseDict
			else:
				return 'Unsupported Post Request Query!'
		else:
			return 'Unsupported Post Request!'
	else:
		return 'Access token Is Required'
			
