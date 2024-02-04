import requests
import datetime
from TwitchUploaderSettings import clipFolder 
from TwitchUploaderSettings import client_Id
from TwitchUploaderSettings import client_Secret
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

# optional, import of Youtube API script to auto-upload the downloaded videos
import YoutubeAPI


def get_token(client_id,client_secret):
    '''retrieves app access token for twitch api using client_id and client_secret'''
    # creates new app access token
    access_response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
    access_token = access_response.json()['access_token']
    return access_token
         

#gathering the urls
def find_videos(token,client_id):
    '''inputs app access token and client id to twitch api, and requests the top X most recent clips'''

    current_time = datetime.datetime.now(datetime.timezone.utc) # creates RFC3339 time of 24 hours before current time.
    yesterday_time = (current_time - datetime.timedelta(days = 1)).isoformat()
    yesterday_time_RFC3339 = yesterday_time[:yesterday_time.index('.')] + 'Z'

    clip_amount = '5' #can be adjusted to less/more clips
    gid = '33214' #currently set to Fortnite, other gameids can be found at https://raw.githubusercontent.com/Nerothos/TwithGameList/master/game_info.csv
    data = {'started_at':yesterday_time_RFC3339,'sort':'views','first':clip_amount,'game_id':gid,'grant_type':'client_credentials'}
    url='https://api.twitch.tv/helix/clips' 

    response = requests.get(url,params=data,headers={"Authorization": "Bearer " + token, "Client-Id": client_id})
    return response.json()  #returns top 5 clips from the last 24h.


def downloadVideos(video_data):
    '''uses selenium to download the gathered clips, and then creates videoItems objects to store the video file + information
    for later upload'''
    driver = webdriver.Chrome()     
    videoItems = []
    print('UPLOADING!')
    for video in video_data:
        driver.get(video["url"])
        sleep(1)    # XPath method is currently absolute as all clips are contained in the same location, (although I may try to improve this later)
        clipPage = driver.switch_to.active_element.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/main/div/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/video")
        videoLink = clipPage.get_attribute("src")  #optaining link with Selenium

        videoFile = requests.get(videoLink)

        with open(f'{clipFolder}{video["id"]}UNEDITED.mp4', 'wb') as f: #creates new file, titled with twitch clip's id + UNEDITED
            f.write(videoFile.content)

        video["id"] = vidInfo(file= f'{clipFolder}{video["id"]}UNEDITED.mp4', title=video["title"], description="", category= "20",keywords="Shorts,Fortnite,FNC",privacyStatus="private")
        videoItems.append(video["id"])  #creating list of vidInfo objects
    print('UPLOAD COMPLETE!')
    return videoItems

class vidInfo():
    '''creates simple object to store basic data about each video for later upload.'''
    def __init__(self,file,title,description,category, keywords, privacyStatus):
        self.file = file
        self.title = title
        self.description = description
        self.category = category
        self.keywords = keywords
        self.privacyStatus = privacyStatus

if __name__ == '__main__':
    access_token = get_token(client_Id,client_Secret) # can be paused if I don't need a new token
    video_info = find_videos(access_token,client_Id) # normally, the first argument is access_token variable
    unedited_videos = downloadVideos(video_info["data"])
    #unedited videos can be then used to either re-edit via DaVinciResolve or upload directly to Youtube.
    
    #optional upload to Youtube using YoutubeAPI.py
    confirm = YoutubeAPI.getService()
    for vid in unedited_videos:
        YoutubeAPI.uploadVideo(youtubeData = confirm, video = vid)