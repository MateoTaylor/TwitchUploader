# TwitchUploader
Twitch.tv is a popular live streaming platform. During 2021, I worked for two months editing and uploading short form clips from Twitch to Youtube. This script automates scraping, editing, and uploading the videos.

TwitchRequests: Gathers the top 5 (or more) most viewed clips from the last 24 hours of a specified Twitch category (currently Fortnite) using Twitch's API, and then downloads the clips as mp4 using Selenium.
Edits clips into a vertical format using moviepy.

Please note the Moviepy module uses an outdated version of PIL, you can avoid issues by downgrading Pillow using
pip install Pillow==9.5.0.

YoutubeUploader: Uploads video files to the Youtube channel with title and other parameters set by data gathered from TwitchRequests.

