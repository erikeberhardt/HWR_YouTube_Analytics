#Install those two things first
#pip install --upgrade google-api-python-client
#pip install --upgrade google-auth-oauthlib google-auth-httplib2

#import the respective library
from googleapiclient.discovery import build

#you can use your api key here (but can also use mine :))
api_key = "AIzaSyCLlldC_cTBAVSzzEY2oEWV6B35cVRBlik"

youtube = build("youtube", "v3", developerKey=api_key)

#I have deactivated the pageToken argument so that you get the first 50 results, feel free to enable it for getting more results
request = youtube.videos().list(
    part="snippet,contentDetails,statistics",
    chart="mostPopular",
#    pageToken="CAoQAA",
    regionCode="US",
    maxResults=50
)

response = request.execute()
print(response)

