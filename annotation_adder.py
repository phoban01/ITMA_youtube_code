import httplib2
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

client_file_path = "/Users/itma/Documents/piaras_scripts/youtube-work/oauth.json"
client_file = open(client_file_path)
client_json = json.load(client_file)
client_file.close()

client_id = client_json['installed']['client_id']
client_secret = client_json['installed']['client_secret']

scope = 'https://www.googleapis.com/auth/youtube'

flow = OAuth2WebServerFlow(client_id,client_secret,scope)

promotion_body = {"items":[
	{
		"id": {
			"type": "website",
			"websiteUrl": "http://www.itma.ie"
		},
		"timing":{
			"offsetMs":1000,
			"type":"offsetFromStart"
		},
		"customMessage": "For more visit:",
		"useSmartTiming":"true"
	}
]}

def main():
	storage = Storage('credentials.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = run(flow,storage)

	http = httplib2.Http()
	http = credentials.authorize(http)

	youtube = build('youtube','v3',http=http)

	channel_response = youtube.channels().list(mine=True,part="invideoPromotion",maxResults=1).execute()

	itma_channel = channel_response["items"][0]

	itma_channel_id = itma_channel["id"]

	try:
		youtube.channels().update(part="invideoPromotion",body=dict(invideoPromotion=promotion_body,id=itma_channel_id)).execute()
	except HttpError,e:
	    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)


	# check if there's been a change
	channel_response = youtube.channels().list(mine=True,part="invideoPromotion",maxResults=1).execute()

	for item in itma_channel.items():
		print item	

if __name__ == '__main__':
  main()