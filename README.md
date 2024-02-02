# TwitchUploader
Current work in progress, attempting to download clips off Twitch, edit, and upload them to Youtube.
Twitch.tv is a popular live streaming platform. During 2021, I worked for two months editing and uploading short form 'clips' from Twitch to Youtube. I'm now curious if I can repeat and automate this process using python.

This is my current project, which is split into three distinct parts:

TwitchRequests: Currently fetches the top 5 most viewed twitch clips of a specified Twitch category (set to Fortnite at the moment, but can be easily moved to whatever category I'd like) using the Twitch API.
Unfortunately, the download links to these clips cannot be accessed with the Twitch API, and must instead be scraped from Twitch's dynamic html. I'm currently learning Selenium to achieve this.

YoutubeUploader: Uploads video files to the Youtube channel, setting their titles and other parameters. Should be able to upload multiple clips and schedule them. Ideally, this means the youtube account will be able to post roughly 1 clip an hour, given than 24 new clips are loaded every day.
