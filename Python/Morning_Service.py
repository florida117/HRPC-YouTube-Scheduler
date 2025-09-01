import os
import sys
import pickle
import time
import pytz
import calendar
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from googleapiclient.http import MediaFileUpload

import logging
logging.basicConfig(level=logging.INFO)

# Sets the location of the home folder
HOME = os.path.expanduser("~")
NOTIFY = os.path.join(HOME, "hrpc_po.sh")  # push notification script

def send_notification(message: str):
    if os.path.isfile(NOTIFY) and os.access(NOTIFY, os.X_OK):
        subprocess.run([NOTIFY, message])
    else:
        print("⚠️ Notification script not found or not executable")

# Function for OAuth authentication
def authenticate(HOME):
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    credentials_file = HOME + "/git/HRPC-YouTube-Scheduler/Python/token.pickle"

    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(HOME + "/git/HRPC-YouTube-Scheduler/Python/client_secret.json", scopes=SCOPES)
        credentials = flow.run_local_server(port=8080)
        with open(credentials_file, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials

# Create an authorized YouTube API client
def create_youtube_client(credentials):
    return build('youtube', 'v3', credentials=credentials)

# Specify your timezone
LOCAL_TZ = pytz.timezone('Europe/Dublin')

def ordinal(n: int):
    if 11 <= (n % 100) <= 13:
        SUFFIX = 'th'
    else:
        SUFFIX = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + SUFFIX

# Calculate the date for next Sunday
TODAY = datetime.now(LOCAL_TZ)
DAYS_AHEAD = 6 - TODAY.weekday()  # 6 is Sunday
if DAYS_AHEAD <= 0:
    DAYS_AHEAD += 7
NEXT_SUNDAY = TODAY + timedelta(days=DAYS_AHEAD)
NEXT_SUNDAY_DAY = ordinal(NEXT_SUNDAY.day)
NEXT_SUNDAY_MONTH = calendar.month_name[NEXT_SUNDAY.month]
NEXT_SUNDAY_YEAR = NEXT_SUNDAY.year

# Set the time to 11 AM
NEXT_SUNDAY = LOCAL_TZ.localize(datetime(NEXT_SUNDAY.year, NEXT_SUNDAY.month, NEXT_SUNDAY.day, 11, 0, 0))

# Convert to UTC
SCHEDULED_START_TIME = NEXT_SUNDAY.astimezone(pytz.UTC)

# Convert to RFC3339 format
SCHEDULED_START_TIME_rfc3339 = SCHEDULED_START_TIME.isoformat()

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
    #print (response["id"])
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
def create_live_broadcast(youtube, video_id, stream_id, HOME, SERVICE_TITLE):
    request = youtube.liveBroadcasts().insert(
        part="snippet,status,contentDetails",
        body={
            "snippet": {
                "title": SERVICE_TITLE,
                "description": "Sunday Service from Hamilton Road Presbyterian Church",
                "scheduledStartTime": SCHEDULED_START_TIME_rfc3339,
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
    BROADCAST_ID = response["id"]

    thumbnail_path = HOME + "/git/HRPC-YouTube-Scheduler/maxresdefault.jpg"
    try:
        request = youtube.thumbnails().set(videoId=BROADCAST_ID, media_body=MediaFileUpload(thumbnail_path))
        response = request.execute()

    except Exception as ex:
        print(f'error: {ex}')

    return BROADCAST_ID

def bind_broadcast(youtube, BROADCAST_ID, stream_id):
  bind_broadcast_response = youtube.liveBroadcasts().bind(
    part="id,contentDetails",
    id=BROADCAST_ID,
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

def write_title(HOME, SERVICE_TITLE):
    f = open(HOME + "/git/HRPC-YouTube-Scheduler/Service_Details/morning_service_title.txt","w")
    f.write(SERVICE_TITLE)
    f.close()

def write_broadcastid(BROADCAST_ID, HOME):
    f = open(HOME + "/git/HRPC-YouTube-Scheduler/Service_Details/morning_service_id.txt","w")
    f.write(BROADCAST_ID)
    f.close()

def main():
    # Authenticate using OAuth
    credentials = authenticate(HOME)

    # Create an authorized client for the YouTube API
    youtube = create_youtube_client(credentials)

    # Create a live stream
    stream_id = "JgRDQzkDs-GgkPgmjNx5Ng1600593527685052"  #create_live_stream(youtube)

    # Get the video ID
    video_id = get_video_id(youtube)

    # Build the service title
    SERVICE_TITLE = "HRPC Sunday Morning Service " + str(NEXT_SUNDAY_DAY) + " " + str(NEXT_SUNDAY_MONTH) + " " + str(NEXT_SUNDAY_YEAR)
    
    # Create a live broadcast
    BROADCAST_ID = create_live_broadcast(youtube, video_id, stream_id, HOME, SERVICE_TITLE)

    # Bind the broadcast to the livestream
    bind_broadcast(youtube, BROADCAST_ID, stream_id)

    # Set the video category to "Nonprofits & Activism"
    category_id = "29"  # This is the ID for "Nonprofits & Activism"
    set_video_category(youtube, BROADCAST_ID, category_id)

    # Write out title and ID
    write_title(HOME, SERVICE_TITLE)
    write_broadcastid(BROADCAST_ID, HOME)

    MSG = f"Morning service scheduled successfully: {SERVICE_TITLE}"
    print(MSG)
    send_notification(MSG)

if __name__ == "__main__":
    main()