import os
import pickle
import sys
import subprocess
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

HOME = os.path.expanduser("~")
NOTIFY = os.path.join(HOME, "hrpc_po.sh")  # push notification script

def send_notification(message: str):
    if os.path.isfile(NOTIFY) and os.access(NOTIFY, os.X_OK):
        subprocess.run([NOTIFY, message])
    else:
        print("⚠️ Notification script not found or not executable")

# Function for OAuth authentication
def authenticate(home_dir):
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    credentials_file = home_dir + "/git/HRPC-YouTube-Scheduler/Python/token.pickle"

    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(home_dir + "/git/HRPC-YouTube-Scheduler/Python/client_secret.json", scopes=SCOPES)
        credentials = flow.run_local_server(port=8080)
        with open(credentials_file, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials

# Create an authorized YouTube API client
def create_youtube_client(credentials):
    return build('youtube', 'v3', credentials=credentials)

def delete_existing_subtitles(video_id, language, home_dir):
    #Delete existing subtitles for a specific language on a video
    credentials = authenticate(home_dir)
    youtube = create_youtube_client(credentials)
    # List existing captions
    request = youtube.captions().list(
        part="id,snippet",
        videoId=video_id
    )
    response = request.execute()

    # Loop through captions and delete those matching the language
    for caption in response.get("items", []):
        if caption["snippet"]["language"] == language:
            caption_id = caption["id"]
            youtube.captions().delete(id=caption_id).execute()
            print(f"Deleted existing subtitle with ID: {caption_id}")

def upload_subtitles(video_id, language, name, subtitle_file_path, home_dir):
    """Upload subtitle file to a YouTube video."""
    credentials = authenticate(home_dir)
    youtube = create_youtube_client(credentials)

    body = {
        'snippet': {
            'videoId': video_id,
            'language': language,
            'name': name
        }
    }

    # Upload the subtitle file
    insert_request = youtube.captions().insert(
        part='snippet',
        body=body,
        media_body=MediaFileUpload(subtitle_file_path, mimetype='application/octet-stream', resumable=True)
    )

    response = insert_request.execute()
    #print(f"Subtitle uploaded: {response}")
    print(f"Subtitle uploaded")

if __name__ == '__main__':
    # Sets the location of the home folder
    home_dir = os.path.expanduser("~")

    # Replace with your video ID, language, name, and path to your .srt file
    f = open(home_dir + "/git/HRPC-YouTube-Scheduler/Service_Details/morning_service_id.txt", "r")
    temp1 = f.readline()
    VIDEO_ID = temp1.strip()
    f.close()

    LANGUAGE = 'en-GB'  # English (United Kingdom)
    f = open(home_dir + "/git/HRPC-YouTube-Scheduler/Service_Details/morning_service_title.txt", "r")
    temp2 = f.readline()
    NAME = temp2.strip()
    f.close()

    delete_existing_subtitles(VIDEO_ID, LANGUAGE, home_dir)
    SUBTITLE_FILE_PATH = (home_dir + "/Documents/Church_Docs/HRPC_Subtitles/" + NAME + ".srt")

    try:
        upload_subtitles(VIDEO_ID, LANGUAGE, NAME, SUBTITLE_FILE_PATH, home_dir)
        msg = f"Morning subtitles successfully uploaded to YouTube for {NAME}"
        print(msg)
        send_notification(msg)
        sys.exit(0)
    except Exception as e:
        err = f"Morning subtitles FAILED uploaded to YouTube for {NAME}"
        print(err, file=sys.stderr)
        send_notification(err)
        sys.exit(1)