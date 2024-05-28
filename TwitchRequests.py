from requests import get, post
from datetime import timedelta,timezone,datetime
from TwitchUploaderSettings import uneditedClipFolder,editedClipFolder,client_Id,client_Secret,titlepng
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from random import choice

from moviepy.editor import VideoFileClip, CompositeVideoClip,concatenate_videoclips,ImageSequenceClip
from moviepy.video.fx.resize import resize
from moviepy.video.fx.crop import crop

#from skimage.filters import gaussian # commented out unless using the blur method on background video.

# optional, import of Youtube API script to auto-upload the downloaded videos
import YoutubeUpload #youtube upload script modified from https://github.com/davidrazmadzeExtra/YouTube_Python3_Upload_Video
from googleapiclient.errors import HttpError


class vidInfo():
    '''creates simple object to store basic data about each video for later upload.'''
    def __init__(self,file,title,description,category, keywords, privacy_status,video_name,duration):
        self.file = file
        self.title = title
        self.description = description
        self.category = category
        self.keywords = keywords
        self.privacy_status = privacy_status
        self.video_name = video_name
        self.duration = duration


def get_token(client_id,client_secret):
    '''retrieves app access token for twitch api using client_id and client_secret'''
    # creates new app access token
    access_response = post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials')
    access_token = access_response.json()['access_token']
    return access_token
         

def find_videos(token,client_id):
    '''inputs app access token and client id to twitch api, and requests the top X most recent clips'''

    # creates RFC3339 time of 24 hours before current time.
    yesterday_time = (current_time - timedelta(days = 1)).isoformat()
    yesterday_time_RFC3339 = yesterday_time[:yesterday_time.index('.')] + 'Z'

    clip_amount = '30' #can be adjusted to less/more clips
    gid = '33214' #currently set to Fortnite, other gameids can be found at https://raw.githubusercontent.com/Nerothos/TwithGameList/master/game_info.csv
    data = {'started_at':yesterday_time_RFC3339,'sort':'views','first':clip_amount,'game_id':gid,'grant_type':'client_credentials'}
    url='https://api.twitch.tv/helix/clips' 

    response = get(url,params=data,headers={"Authorization": "Bearer " + token, "Client-Id": client_id})
    return response.json()  #returns top 5 clips from the last 24h.


def download_videos(video_data):
    '''uses selenium to download the gathered clips, and then creates videoItems objects to store the video file + information
    for later upload'''
    driver = webdriver.Chrome()     
    videoItems = []
    for video in video_data:
        if video["language"] == "en" and int(video["duration"]) >= 10 :
            driver.get(video["url"])
            sleep(0.5)    # XPath method is currently absolute as all clips are contained in the same location, (although I may try to improve this later)
            xp = "/html/body/div[1]/div/div[1]/div/div[3]/div/div/main/div/div/div[2]/div[1]/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/video"
            clipPage = driver.switch_to.active_element.find_element(By.XPATH, xp)
            videoLink = clipPage.get_attribute("src")  # optaining link with Selenium

            videoFile = get(videoLink) # video link isn't directly downloadable, so we need to open it up with requests first

            with open(f'{uneditedClipFolder}{video["id"]}UNEDITED.mp4', 'wb') as f: # creates new file, titled with twitch clip's id + UNEDITED
                f.write(videoFile.content)

            video["id"] = vidInfo(file= f'{uneditedClipFolder}{video["id"]}UNEDITED.mp4', title=title_creator(video["broadcaster_name"])    , 
                                description="#shorts #fortnite #twitch SUB FOR MORE", category= "20",
                                keywords="Shorts,Fortnite,FNCS,Tenz,Tarik,Ninja,Funny,Skibidi,fyp,Update,Clip,Moment,Daily moments,Clix insane moments,Poopy,peepee,farts,clix trolling,",
                                privacy_status="public",video_name=video["id"],duration=video["duration"])
            videoItems.append(video["id"])  #creating list of vidInfo objests
    return videoItems

def title_creator(streamer_name):
    current_time = datetime.now(timezone.utc)
    options = [f"I Can't Believe {streamer_name} Did This", f"This Is Why {streamer_name} Is The GOAT",
               f"THIS Is How You Play Fortnite | {streamer_name}", f"{streamer_name} HAS to be stopped",
               f"Why You Should Play Like {streamer_name}", f"THIS is what a PRO looks like / {streamer_name}",
               f"{streamer_name} Is Bringing OG Fortnite BACK", f"{streamer_name} Pops Off", f"{streamer_name} Just Broke Fortnite",
               f"Best Fortnite Moments of {current_time.month}/{current_time.day} | {streamer_name}",
               f"Top Fortnite Clips of {current_time.month}/{current_time.day} | {streamer_name}",
               f"Top Fortnite Livestreams of {current_time.month}/{current_time.day} | {streamer_name}"]
    return choice(options)
        

def combine_videos(clip_list):
    '''combines list of clips into ~30second videos.'''
    combined_clip_list = []
    while len(clip_list) > 0:
        if clip_list[0].duration < 8:
            del clip_list[0]
        else:
            temp = [clip_list[0]]
            dur = clip_list[0].duration
            if dur < 25 and len(clip_list)>1:
                for second_clip in clip_list:
                    if second_clip not in temp and (dur + second_clip.duration) < 40:
                        temp.append(second_clip)
                        dur += second_clip.duration
            for x in temp:
                clip_list.remove(x)
            combined_clip_list.append(temp)
    return combined_clip_list
                
def blur(image): 
    """ Returns a blurred (radius=8 pixels) version of the image 
    Source: https://zulko.github.io/moviepy/examples/quick_recipes.html"""  
    #currently not using this because my laptop is slow, but it is an option and generally looks better  
    #return gaussian(image.astype(float), sigma=8)

def edit_videos(combined_clip_list):
    '''
    Uses moviepy to take a clip and edit it into a 1920x1080 format for YoutubeShorts. Clip is then placed into a new folder.
    however Moviepy uses an outdated version of PIL, you can avoid issues by downgrading Pillow using
    pip install Pillow==9.5.0, or manually replacing the ANTIALIAS attributes within moviepy with Image.LANCZOS
    '''
    output_height = 1920
    output_width = 1080
    return_list = []
    for c in combined_clip_list[:6]:
        #combining clips into connectated videos
        clip_name = f"{editedClipFolder}{c[0].video_name}EDITED.mp4"    
        videofileclip_list = []     
        for clip in c:
            if clip.duration < 59:
                videofileclip_list.append(VideoFileClip(clip.file))
            else:
                videofileclip_list.append(VideoFileClip(clip.file).subclip(0,5))
        clip_video = concatenate_videoclips(videofileclip_list)
    
        #zooming original video in slightly and cropping it to screen width.
        clip_video_resized = resize(clip_video, width = output_width*1.1)
        #clip_video_cropped = crop(clip_video_resized,x1 = output_width*.05,x2= output_width*1.05)

        #background video, can be any file (I prefer a zoomed version of the original clip), but can also be black screen etc.
        background_video = concatenate_videoclips(videofileclip_list)
        background_video_resized = resize(background_video, height = output_height)


        #background_video_blurred = background_video_resized.fl_image( blur ) 
        #commented out because blurring is very resource intensive

        #background width now equals background_height*16/9, we want to cut this down to 1080.
        background_video_cropped = crop(background_video_resized, x1=(output_height*(16/9)-1080)/2,x2=(output_height*(16/9)-1080)/2+1080)

        # now we add a small title
        title_video = ImageSequenceClip([titlepng], durations=[background_video_cropped.duration],load_images=True)

        combined_clips = CompositeVideoClip([background_video_cropped,clip_video_resized.set_position('center'),title_video])
        combined_clips.write_videofile(clip_name,codec = "libx264",fps = 60)

        combined_clips.close()
        title_video.close()
        background_video.close()
        clip_video.close()

        c[0].file = f"{editedClipFolder}{c[0].video_name}EDITED.mp4"
        print("File location:" + c[0].file)
        return_list.append(c[0])
    return return_list #returns a list of vidinfo files for YoutubeUpload.py to upload.


if __name__ == '__main__':
    #finding top clips with twitch API
    print("ACCESSING TWITCH API")
    access_token = get_token(client_Id,client_Secret) # can be paused if I don't need a new token
    current_time = datetime.now(timezone.utc)
    video_info = find_videos(access_token,client_Id) # normally, the first argument is access_token variable
    #print(video_info['data']) #useful line to understand what data twitch API is grabbing
    print("TWITCH DATA FOUND")

    # scraping videos from the twitch website
    print("DOWNLOADING VIDEOS")
    downloaded_videos = download_videos(video_info["data"])
    print("DOWNLOADED!")

    #combining scraped video files into lists of 25-60sec
    print("COMBINING VIDEOS")
    combined_videos = combine_videos(downloaded_videos)
    print("COMBINED!")
    
     #turning video vertical, combining it with background, and moving to a new folder
    print("EDITING VIDEOS!")
    edited_videos = edit_videos(combined_videos)
    print("EDITED!")

    #optional upload to Youtube using YoutubeAPI.py
    print("UPLOADING VIDEOS!")
    confirm = YoutubeUpload.get_authenticated_service()
        
    for vid in enumerate(edited_videos):
        try:
            upload_time = (current_time + timedelta(hours = vid[0])).astimezone().isoformat()
            YoutubeUpload.initialize_upload(confirm, vid[1], upload_time)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
    
    print("UPLOADED, PROCESS COMPLETE")
