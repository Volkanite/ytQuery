import urllib
import json
from optparse import OptionParser
from urllib.request import urlopen

parser = OptionParser()
parser.add_option('-u', '--user', dest='user', help='The YouTube username',default=None)
parser.add_option('-c', '--channel', dest='channel', help='Gets the channel ID a video belongs to',default=None)
parser.add_option('-q', '--query', dest='query', help='Video query',default=None)
parser.add_option('-p', '--playlist', dest='playlist', help='The Playlist Id',default=None)
parser.add_option('-o', '--uploads', dest='uploads', help='Gets the uploads playlist from a channel ID',default=None)

(options, args) = parser.parse_args()
Options_user = options.user
Options_channel = options.channel
Options_query = options.query
Options_playlist = options.playlist
Options_uploads = options.uploads

#An api key is needed for v3 of the Google api. In v2 we could do this anonymously but now that v2 is
#deprecated I had to upgrade(still upgrading actually) to v3 and with every convenience (for Google 
#in this case) comes an inconvenience for someone else. I provided my api key for convenience (which 
#is an inconvenience for me) as I find it quite silly for a user having to create a Google account
#just so they can get an api key to use this little script. Please don't spam my key. If you can, I 
#recommend you get your own free key @ https://code.google.com/apis/console For help check 
#https://www.youtube.com/watch?v=JbWnRhHfTDA

apiKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

#DEBUG
#print query


def GetJson(url):

    #print(url)

    data = urlopen(url)
    json_data = json.loads(data.read())
    
    if 'error' in json_data:

        message = json_data['error']['message']

        if message == "API key expired. Please renew the API key.":
            print('ERROR: API key expired!')
        elif message == "API key not valid. Please pass a valid API key.":
            print('ERROR: API key is invalid! Did you remember to set it!?')
        else:
            print(message)
        
        return None
            
    return json_data


def GetEntries(url):
    return GetJson(url)['feed']['entry']

    
def GetUrlUser( User, MaxResults, StartIndex ):
    
    url = "https://gdata.youtube.com/feeds/api/users/%s/uploads" \
        "?max-results=%d" \
        "&start-index=%d" \
        "&v=2" \
        "&alt=json" %(Options_user, maxResults, startIndex)
        
    return url

    
def GetUrlPlaylist( Playlist, MaxResults, StartIndex ):

    url = "https://gdata.youtube.com/feeds/api/playlists/%s" \
        "?max-results=%d" \
        "&start-index=%d" \
        "&v=2" \
        "&alt=json" % (Playlist, MaxResults, StartIndex)
        
    return url
    

def GetUrlQuery( Query, MaxResults, StartIndex ):

    queryItems = query.split()
    queryFormat = ""
    queryItemCount = 0
    
    for word in queryItems:
        if queryItemCount > 0:
            queryFormat += "+"
        
        queryFormat += word
        queryItemCount += 1
    
    url = "https://gdata.youtube.com/feeds/api/videos" \
    "?q=%s" \
    "&max-results=%d" \
    "&start-index=%d" \
    "&v=2" \
    "&alt=json" %(queryFormat, maxResults, startIndex)
    
    return url
    

def GetPlaylistVideoCount( PlaylistId ):
    
    url = "https://www.googleapis.com/youtube/v3/playlistItems" \
    "?part=snippet" \
    "&maxResults=0" \
    "&playlistId=%s" \
    "&key=%s" % (PlaylistId, apiKey)
    
    return GetJson(url)['pageInfo']['totalResults']

    
def GetPlaylistName( PlaylistId ):

    url = "https://www.googleapis.com/youtube/v3/playlists?part=snippet,localizations" \
            "&id=%s" \
            "&fields=items(localizations,snippet/localized/title)" \
            "&key=%s" % (PlaylistId, apiKey)
        
    return GetJson(url)['items'][0]['snippet']['localized']['title']

    
def GetUploadsPlaylistId ( User ):

    url = "https://www.googleapis.com/youtube/v3/channels" \
        "?part=contentDetails" \
        "&forUsername=%s" \
        "&key=%s" % (User, apiKey)
            
    response = GetJson(url)
    
    if response:
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    else:
        return None
    

def GetUploadsPlaylistIdForChannel ( Id ):

    url = "https://www.googleapis.com/youtube/v3/channels" \
        "?part=contentDetails" \
        "&id=%s" \
        "&key=%s" % (Id, apiKey)
        
    return GetJson(url)['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    

def GetPlaylist( PlaylistId, PageToken ):
    
    url = "https://www.googleapis.com/youtube/v3/playlistItems" \
    "?part=snippet" \
    "&maxResults=50" \
    "&pageToken=%s" \
    "&playlistId=%s" \
    "&key=%s" % (PageToken, PlaylistId, apiKey)
    
    return GetJson(url)
	

def GetVideoOwner( VideoId ):
	
	url = "https://www.googleapis.com/youtube/v3/videos" \
	"?part=snippet" \
	"&id=%s" \
	"&key=%s" % (VideoId, apiKey)
	
	response = GetJson(url)
	
	if response and 'items' in response:
	    return response['items'][0]['snippet']['channelId']
	else:
	    return "ERROR: Invalid Response"


maxResults = 50
startIndex = 0
numVideos = 0
entries = []
PlaylistId = ""
NextPageToken = ""
fileName = ""
ready = 0

if apiKey != "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
    ready = 1
else:
    print("Please update API key!!!") 

if ready:
    if Options_user:
        PlaylistId = GetUploadsPlaylistId(Options_user)
    if Options_uploads:
        PlaylistId = GetUploadsPlaylistIdForChannel(Options_uploads)
    if Options_playlist:
        PlaylistId = Options_playlist
    if Options_query:
        numVideos = 500

#get number of videos
if PlaylistId and numVideos == 0:
    numVideos = GetPlaylistVideoCount(PlaylistId)


while PlaylistId:

    #can't start at 0
    if startIndex == 0:
        startIndex = 1
    
    if Options_user:
        url = GetUrlUser(Options_user, maxResults, startIndex)
        
    if Options_query:
        url = GetUrlQuery(Options_query, maxResults, startIndex)
        
    if Options_playlist:
        url = GetUrlPlaylist(Options_playlist, maxResults, startIndex)
    
    #revert if was 0    
    if startIndex == 1:
        startIndex = 0
        
    playlistJSON = GetPlaylist(PlaylistId, NextPageToken)
    
    if 'nextPageToken' in playlistJSON:
        NextPageToken = playlistJSON['nextPageToken']
        
    entries = playlistJSON['items']
  
    for entry in entries:
            title = entry['snippet']['title']
            title = title.encode('utf8', 'ignore')
            link = "https://www.youtube.com/watch?v=%s" % (entry['snippet']['resourceId']['videoId'])
            
            print(title)
            print(link)
            print("\n")

    if (startIndex + len(entries)) >= numVideos:
        break
        
    startIndex += maxResults
    
    #progress
    print("%d / %d" %(startIndex, numVideos))
    
    #cant query beyond 500 items
    if Options_query and startIndex >= 500:
        break

if ready:  
    if Options_user:
        fileName = Options_user
    if Options_channel:
        fileName = Options_channel
    if Options_query:
        fileName = Options_query
    if Options_playlist:
        fileName = GetPlaylistName(Options_playlist)
    if Options_channel:
        print(GetVideoOwner(Options_channel))
