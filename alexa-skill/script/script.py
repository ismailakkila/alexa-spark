import sparkApi
from sys import argv

sparkApi.sparkAccessToken = argv[1]
for roomItem in sparkApi.get('rooms')['items']:
	print roomItem['title']