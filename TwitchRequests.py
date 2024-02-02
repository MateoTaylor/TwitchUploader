import requests
import datetime
from TwitchScraperSettings import client_Id
from TwitchScraperSettings import client_Secret
 # imports cliend id and client secret


def get_token(client_id,client_secret):
    '''retrieves app access token for twitch api using client_id and client_secret'''
    # for user key 
    #access_response = requests.post('https://id.twitch.tv/oauth2/authorize?client_id=pugl2bjiikyov3y9knomc87w5ttiz2&redirect_uri=http://localhost&response_type=token&scope=clips:edit')
    #access_token= 'jkenwsly3n6exxotokiqp5cq53p2e3' # user key that I generated with my acc

    access_response = requests.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
    access_token = access_response.json()['access_token']
    return access_token
         

#gathering the urls
def find_videos(token,client_id):
    '''inputs app access token and client id to twitch api, and requests the top 5 most recent clips'''

    current_time = datetime.datetime.now(datetime.timezone.utc)
    yesterday_time = (current_time - datetime.timedelta(days = 1)).isoformat()
    yesterday_time_RFC3339 = yesterday_time[:yesterday_time.index('.')] + 'Z'

    data = {'started_at':yesterday_time_RFC3339,'sort':'views','first':'5','game_id':'33214','grant_type':'client_credentials'}
    url='https://api.twitch.tv/helix/clips'

    response = requests.get(url,params=data,headers={"Authorization": "Bearer " + token, "Client-Id": client_id})
    return response.json()

def download_videos(video_links):
    response = requests.get(video_links[0])

    
        
#MAIN   
    
# access_token = get_token(client_Id,client_Secret) paused as I don't need a new token
video_info = find_videos('1avr5fxtl7wzwg6v0c0asx90lkakir',client_Id) # normally, the first argument is access_token variable
video_links = []
for video in video_info['data']:
    video_links.append(video['url'])
download_videos(video_links)
print(video_links)
    
    
