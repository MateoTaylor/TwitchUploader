from TwitchUploaderSettings import yt_auth_line
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

SCOPES =['https://www.googleapis.com/auth/youtube.upload','https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

class vidInfo():
    def __init__(self,file,title,description,category, keywords, privacyStatus):
        self.file = file
        self.title = title
        self.description = description
        self.category = category
        self.keywords = keywords
        self.privacyStatus = privacyStatus

def getService():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(yt_auth_line, scopes = SCOPES)
    credentials = flow.run_local_server()
    return build(API_SERVICE_NAME, API_VERSION, credentials= credentials)


def uploadVideo(youtubeData,video):

    body = {
    "snippet": {
        "title": video.title,
        "description": video.description,
        "tags": video.keywords,
        "categoryId": video.category},
        "status": video.privacyStatus}
    
    url = "https://www.googleapis.com/youtube/v3/videos"
    part = ",".join(body.keys()),

    request = youtubeData.videos().insert(part = part,body = body)
    media_body=MediaFileUpload(video.file, chunksize=-1)