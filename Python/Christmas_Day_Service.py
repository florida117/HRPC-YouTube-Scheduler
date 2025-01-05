import os
import sys
import pickle
import time
import pytz
import calendar
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from googleapiclient.http import MediaFileUpload

import logging
logging.basicConfig(level=logging.INFO)

# Function for OAuth authentication
def authenticate(home_dir):
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    credentials_file = home_dir + '/yt-dlp/HRPC_Python/token.pickle'

    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(home_dir + '/yt-dlp/HRPC_Python/client_secret.json', scopes=SCOPES)
        credentials = flow.run_local_server(port=8080)
        with open(credentials_file, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials

# Create an authorized YouTube API client
def create_youtube_client(credentials):
    return build('youtube', 'v3', credentials=credentials)

# Specify your timezone
local_tz = pytz.timezone('Europe/Dublin')

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

# Calculate the date for next Sunday
#today = datetime.now(local_tz)
#days_ahead = 6 - today.weekday()  # 6 is Sunday
#if days_ahead <= 0:
#    days_ahead += 7
#next_sunday = today + timedelta(days=days_ahead)
#next_sunday_day = ordinal(next_sunday.day)
#next_sunday_month = calendar.month_name[next_sunday.month]
now = datetime.now(local_tz)
this_year = now.year
christmas = datetime(now.year, 12, 25, 10, 0)
# Set the time to 11 AM
#next_sunday = next_sunday.replace(hour=10, minute=0, second=0, microsecond=0)

# Convert to UTC
scheduled_start_time = christmas.astimezone(pytz.UTC)

# Convert to RFC3339 format
scheduled_start_time_rfc3339 = scheduled_start_time.isoformat()

# Create a live stream
def create_live_stream(youtube):
    request = youtube.liveStreams().insert(
        part="snippet,cdn,contentDetails,status",
        body={
            "snippet": {
                "title": "HRPC Livestream",
                #"description": "A description of your video stream. This field is optional."
            },
            "cdn": {
                "frameRate": "variable",
                "ingestionType": "rtmp",
                "resolution": "variable"
            },
            "contentDetails": {
                "enableAutoStart": False,
                "isReusable": True
            }
        }
    )
    response = request.execute()
    print (response["id"])
    return response["id"]

# New function to set the video category
def set_video_category(youtube, video_id, category_id):
    try:
        # First, get the existing video details
        video_response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if not video_response['items']:
            logging.error(f"Video with ID {video_id} not found.")
            return None

        # Get the existing snippet
        snippet = video_response['items'][0]['snippet']

        # Update only the categoryId
        snippet['categoryId'] = category_id

        # Now update the video with the modified snippet
        request = youtube.videos().update(
            part="snippet",
            body={
                "id": video_id,
                "snippet": snippet
            }
        )
        response = request.execute()
        logging.info(f"Category set successfully for video ID: {video_id}")
        return response
    except Exception as e:
        logging.error(f"Error setting video category: {e}")
        raise

# Create a live broadcast
def create_live_broadcast(youtube, video_id, stream_id, home_dir):
    request = youtube.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body={
            "snippet": {
                "title": "HRPC Christmas Morning Service" + " " + str(this_year) ,
                "description": "Christmas Morning Service from Hamilton Road Presbyterian Church",
                "scheduledStartTime": scheduled_start_time_rfc3339,
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": "false"
            },
            "contentDetails": {
                "enableAutoStart": False
            }
        }
    )
    response = request.execute()
    broadcast_id = response["id"]

    thumbnail_path = home_dir + "/yt-dlp/maxresdefault.jpg"
    try:
        request = youtube.thumbnails().set(videoId=broadcast_id, media_body=MediaFileUpload(thumbnail_path))
        response = request.execute()
        #print(response)
    except Exception as ex:
        print(f'error: {ex}')

    return broadcast_id

def bind_broadcast(youtube, broadcast_id, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=broadcast_id,
    streamId=stream_id
  ).execute()

# Get the video ID from your channel
def get_video_id(youtube):
    request = youtube.liveBroadcasts().list(
        part="contentDetails",
        broadcastStatus="upcoming",
        broadcastType="all",
        maxResults=100
        )
    response = request.execute()

    # Parse the response
    videos = response.get('items', [])

def write_title(home_dir):
    f = open(home_dir + "/yt-dlp/christmas_service_title.txt","w")
    f.write("HRPC Christmas Morning Service" + " " + str(this_year))
    f.close()

def write_broadcastid(broadcast_id, home_dir):
    f = open(home_dir + "/yt-dlp/christmas_service_id.txt","w")
    f.write(broadcast_id)
    f.close()

def main():
    # Sets the location of the home folder
    home_dir = os.path.expanduser("~")

    # Authenticate using OAuth
    credentials = authenticate(home_dir)

    # Create an authorized client for the YouTube API
    youtube = create_youtube_client(credentials)

    # Create a live stream
    stream_id = "JgRDQzkDs-GgkPgmjNx5Ng1600593527685052"  #create_live_stream(youtube)

    # Get the video ID
    video_id = get_video_id(youtube)

    # Create a live broadcast
    broadcast_id = create_live_broadcast(youtube, video_id, stream_id, home_dir)

    # Bind the broadcast to the livestream
    bind_broadcast(youtube, broadcast_id, stream_id)

    # Set the video category to "Nonprofits & Activism"
    category_id = "29"  # This is the ID for "Nonprofits & Activism"
    set_video_category(youtube, broadcast_id, category_id)

    # Write out title and ID
    write_title(home_dir)
    write_broadcastid(broadcast_id, home_dir)

    print("Live broadcast has been successfully created and categorized as Nonprofits & Activism.")

if __name__ == "__main__":
    main()

