# TwitchUploader
Current work in progress, attempting to download clips off Twitch, edit, and upload them to Youtube.
Twitch.tv is a popular live streaming platform. During 2021, I worked for two months editing and uploading short form 'clips' from Twitch to Youtube. I'm now curious if I can repeat and automate this process using python.

This is my current project, which is split into three distinct parts:

TwitchRequests: Gathers the top 5 (or more) most viewed clips from the last 24 hours of a specified Twitch category (currently Fortnite) using Twitch's API, and then downloads the clips as mp4 using Selenium. (completed)

DaVinciResolveEditor: interacts with the DaVinci resolve api to take clips downloaded from TwitchRequests and edit them into a vertical format suitable for Youtube Shorts content (work in progress)

YoutubeUploader: Uploads video files to the Youtube channel, setting their titles and other parameters. (completed)
