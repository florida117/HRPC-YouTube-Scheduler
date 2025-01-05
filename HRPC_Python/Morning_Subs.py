import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Function for OAuth authentication
def authenticate(home_dir):
    SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    credentials_file =home_dir + "/yt-dlp/HRPC_Python/token.pickle"

    if os.path.exists(credentials_file):
        with open(credentials_file, 'rb') as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(home_dir + "/yt-dlp/HRPC_Python/client_secret.json", scopes=SCOPES)
        credentials = flow.run_local_server(port=8080)
        with open(credentials_file, 'wb') as token:
            pickle.dump(credentials, token)
    return credentials

# Create an authorized YouTube API client
def create_youtube_client(credentials):
    return build('youtube', 'v3', credentials=credentials)

def delete_existing_subtitles(video_id, language):
    #Delete existing subtitles for a specific language on a video
    credentials = authenticate()
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

def upload_subtitles(video_id, language, name, subtitle_file_path):
    """Upload subtitle file to a YouTube video."""
    credentials = authenticate()
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
    f = open(home_dir + "/yt-dlp/morning_service_id.txt", "r")
    temp1 = f.readline()
    VIDEO_ID = temp1.strip()
    f.close()

    LANGUAGE = 'en-GB'  # English (United Kingdom)
    f = open(home_dir + "/yt-dlp/morning_service_title.txt", "r")
    temp2 = f.readline()
    NAME = temp2.strip()
    f.close()

    delete_existing_subtitles(VIDEO_ID, LANGUAGE)
    SUBTITLE_FILE_PATH = (home_dir + "/Documents/Church_Docs/HRPC_Subtitles/" + NAME + ".srt")
    upload_subtitles(VIDEO_ID, LANGUAGE, NAME, SUBTITLE_FILE_PATH)